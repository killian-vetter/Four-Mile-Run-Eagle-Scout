## directory to build lambda function in Python
The use of pipenv is experimental; this gets the job done, but it's unclear whether it's the best tool.

## Getting started
Make sure you're setup with VirtualBox and Vagrant.  Create vagrant box with `vagrant up`

If you just want to edit lambda_function.py and deploy new version without adding any new dependancies you can do the following.

```
# create directory that will become the .zip
mkdir output

# install pipenv and prepare the python3.7 environment
python3.7 -m pip install --user pipenv
python3.7 -m pipenv --python 3.7

# install the dependancies into output directory based on requirements.txt file
python3.7 -m pip install -r requirements.txt --no-deps -t output

# zip up the output directory
cd output
zip -r ../output.zip .
cd ..
# the above commands are only necessary for the first time creating the zip
# subsequent changes to the lambda_function.py file only need to do the following.

# add the lambda_function.py file
zip -g output.zip lambda_function.py
```

This will produce the zip file that can be uploaded to aws.

## Adding new dependencies
First let pipenv know about the new dependency by:
```
python3.7 -m pipenv install <newdep>
```

Then generate new requierements.txt
```
python3.7 -m pipenv lock -r > requirements.txt
```
The continue the above steps starting with the `install -r requirements.txt` line.

## Remarks
I feel like if I have to generate the requirements.txt file it's probably just easier to use virtualenv instead of pipenv.  I also hear https://github.com/sdispater/poetry is good.