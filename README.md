# see doc

http://doc.lonxun.com/PWMLFF/Appendix-2/

pip3 install setuptools wheel twine

rm dist/ -r
python3 setup.py sdist bdist_wheel
twine upload dist/* --verbose

