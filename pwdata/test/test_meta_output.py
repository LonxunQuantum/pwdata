import numpy as np
import pytest
from pathlib import Path

from pwdata.config import Config
from pwdata.convert_files import image_to_atomrow, save_to_meta
from pwdata.image import Image
from pwdata.main import run_convert_configs


EXTXYZ_FRAME = """2
Lattice=\"3.0 0.0 0.0 0.0 4.0 0.0 0.0 0.0 5.0\" Properties=species:S:1:pos:R:3:forces:R:3 energy=-1.25 virial=\"1.0 0.2 0.3 0.2 2.0 0.4 0.3 0.4 3.0\" pbc=\"T F T\"
H 0.1 0.2 0.3 1.0 2.0 3.0
O 1.1 1.2 1.3 -1.0 -2.0 -3.0
"""


def make_image(lattice=None, energy=-1.0, force=None, virial=None):
    return Image(
        atom_nums=1,
        atom_types_image=[1],
        lattice=np.eye(3) if lattice is None else lattice,
        position=[[0.0, 0.0, 0.0]],
        force=[[0.0, 0.0, 0.0]] if force is None else force,
        Ep=energy,
        virial=np.eye(3) if virial is None else virial,
        pbc=[True, True, True],
        cartesian=True,
    )


def test_cvt_configs_writes_meta_database_readable_by_pwdata(tmp_path):
    source = tmp_path / "input.xyz"
    output_dir = tmp_path / "output"
    source.write_text(EXTXYZ_FRAME, encoding="utf-8")
    source_image = Config(data_path=str(source), format="extxyz").images[0]

    run_convert_configs(
        [
            "-i",
            str(source),
            "-f",
            "extxyz",
            "-s",
            str(output_dir),
            "-o",
            "meta",
        ]
    )

    output_file = output_dir / "dataset.aselmdb"
    assert output_file.is_file()

    converted = Config(data_path=str(output_file), format="meta")
    assert len(converted.images) == 1
    image = converted.images[0]

    np.testing.assert_array_equal(image.atom_types_image, [1, 8])
    np.testing.assert_allclose(image.lattice, np.diag([3.0, 4.0, 5.0]))
    np.testing.assert_allclose(
        image.position, [[0.1, 0.2, 0.3], [1.1, 1.2, 1.3]]
    )
    np.testing.assert_array_equal(image.pbc, source_image.pbc)
    assert image.Ep == -1.25
    np.testing.assert_allclose(
        image.force, [[1.0, 2.0, 3.0], [-1.0, -2.0, -3.0]]
    )
    np.testing.assert_allclose(
        image.virial, [[1.0, 0.2, 0.3], [0.2, 2.0, 0.4], [0.3, 0.4, 3.0]]
    )


def test_cvt_configs_rejects_unmerged_meta_output(tmp_path):
    source = tmp_path / "input.xyz"
    source.write_text(EXTXYZ_FRAME, encoding="utf-8")

    with pytest.raises(ValueError, match="META output requires -m 1"):
        run_convert_configs(
            [
                "-i",
                str(source),
                "-f",
                "extxyz",
                "-s",
                str(tmp_path / "output"),
                "-o",
                "meta",
                "-m",
                "0",
            ]
        )


def test_cvt_configs_converts_pwmlff_npy_to_meta(tmp_path):
    source = Path(__file__).parents[2] / "examples" / "pwmlff_data" / "LiSiC" / "C2"
    output_dir = tmp_path / "output"
    expected = Config(data_path=str(source), format="pwmlff/npy")

    run_convert_configs(
        [
            "-i",
            str(source),
            "-f",
            "pwmlff/npy",
            "-s",
            str(output_dir),
            "-o",
            "meta",
        ]
    )

    converted = Config(
        data_path=str(output_dir / "dataset.aselmdb"), format="meta"
    )
    assert len(converted.images) == len(expected.images) == 15
    np.testing.assert_array_equal(
        converted.images[0].atom_types_image, expected.images[0].atom_types_image
    )
    expected_position = expected.images[0].position
    if not expected.images[0].cartesian:
        expected_position = np.dot(expected_position, expected.images[0].lattice)
    np.testing.assert_allclose(converted.images[0].position, expected_position)
    np.testing.assert_allclose(converted.images[0].force, expected.images[0].force)
    np.testing.assert_allclose(converted.images[0].virial, expected.images[0].virial)
    assert converted.images[0].Ep == expected.images[0].Ep


def test_cvt_configs_refuses_to_append_to_existing_meta_database(tmp_path):
    source = tmp_path / "input.xyz"
    output_dir = tmp_path / "output"
    source.write_text(EXTXYZ_FRAME, encoding="utf-8")
    args = [
        "-i",
        str(source),
        "-f",
        "extxyz",
        "-s",
        str(output_dir),
        "-o",
        "meta",
    ]
    run_convert_configs(args)

    with pytest.raises(FileExistsError, match="already exists"):
        run_convert_configs(args)

    converted = Config(
        data_path=str(output_dir / "dataset.aselmdb"), format="meta"
    )
    assert len(converted.images) == 1


@pytest.mark.parametrize(
    ("energy", "force", "missing_label"),
    [(None, [[0.0, 0.0, 0.0]], "energy"), (-1.0, None, "forces")],
)
def test_meta_output_rejects_missing_training_labels(energy, force, missing_label):
    image = make_image(energy=energy, force=force)
    if missing_label == "forces":
        image.force = None

    with pytest.raises(ValueError, match="requires {}".format(missing_label)):
        image_to_atomrow(image)


def test_meta_output_rejects_asymmetric_virial():
    image = make_image(
        virial=[[1.0, 0.2, 0.0], [0.4, 2.0, 0.0], [0.0, 0.0, 3.0]]
    )

    with pytest.raises(ValueError, match="symmetric virial"):
        image_to_atomrow(image)


def test_meta_output_removes_partial_database_after_failure(tmp_path):
    valid_image = make_image()
    invalid_image = make_image(lattice=np.zeros((3, 3)))

    with pytest.raises(ValueError, match="zero-volume cell"):
        save_to_meta(tmp_path, [valid_image, invalid_image])

    assert not (tmp_path / "dataset.aselmdb").exists()
    assert list(tmp_path.iterdir()) == []
