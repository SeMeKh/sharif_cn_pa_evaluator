To setup the test environment:
0. Change your current directory to the same directory containing this README.
	cd /path/to/here
1. Install dependencies:
	apt-get install valgrind python-virtualenv
2. Setup the virtualenv:
	virtualenv -p $(which python2) venv
3. Activate the virtualenv:
	source venv/bin/activate
4. Upgrade `pip` and `setuptools`:
    pip install -U pip setuptools
5. Install python requirements:
	pip install -r requirements.txt

To run the tests:
0. Activate the virtualenv:
	source venv/bin/activate
1. Run the evaluation script by running:
	./run.py pa_40443_941_0 run --student_bin /path/to/your/sdp.out

Please note that you can only run your own codes and have not access to the model solution.
