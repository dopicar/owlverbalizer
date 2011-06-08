# OWL verbalizer tester
# Kaarel Kaljurand
# 2011-06-07
#
# Verbalizes all the OWL files in a given directory either
# using the OWL verbalizer commandline script or the HTTP server (via curl).
# Saves the outputs into files so that they can be compared against the
# gold standard.
#
# Work in progress
#
# Example:
#
# python run_tests.py --in examples --mode http
#
# TODO:
# * commandline arguments
# * performance measurement
# * instead of curl use some Python library for better performance
#
import sys
import argparse
import subprocess
import threading
import os
import re
import time
from os.path import join

owl_to_ace_exe="./owl_to_ace.exe"
curl='curl'
extension_pattern='\.owl'
port=5123
server_url="http://localhost:" + str(port)


def wait_until_up(server):
	"""
	TODO: we need something more sophisticated here,
	e.g. wait until the first line becomes available on STDOUT.
	"""
	time.sleep(2)


def post_files_with_curl(g):
	"""
	"""
	for path in g:
		cmd = [curl, '-s', '-S', '-F', "xml=@" + path, server_url]
		process_file(cmd, path)


def process_file(cmd, path):
	if args.parallel:
		t = threading.Thread(target=process_file_aux, args=[cmd, path])
		t.setDaemon(True)
		t.start()
	else:
		process_file_aux(cmd, path)


def process_file_aux(cmd, path):
	basename, extension = os.path.splitext(path)
	ace_path = basename + ".ace.txt"
	f = open(ace_path, 'w')
	pipe = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=f)
	ret_code = pipe.wait()
	f.flush()
	f.close()
	print 'Verbalized:', path


def run_as_script(g):
	"""
	"""
	for path in g:
		cmd = [owl_to_ace_exe, '-owlfile', path]
		process_file(cmd, path)


def owl_file_generator(top):
	"""
	Generates relative pathnames that correspond to
	files with the extension $extension_pattern in the given directory.
	"""
	for root, dirs, files in os.walk(top):
		for name in files:
			path = os.path.join(root, name)
			basename, extension = os.path.splitext(path)
			if re.match(extension_pattern, extension):
				yield path


parser = argparse.ArgumentParser(description='Run OWL verbalizer tests.')

parser.add_argument('-i', '--in', type=str, action='store', dest='dir_in',
                   help='set the directory that contains the input OWL/XML files (OBLIGATORY)')

parser.add_argument('-m', '--mode', type=str, action='store', dest='mode',
                   default="cli",
                   help='set the service mode, one of {cli, http} (default: cli)')

parser.add_argument('-p', '--parallel', action='store_true', dest='parallel', default=False,
                   help='run the tests in parallel (default: false)')

parser.add_argument('-f', '--fmt', type=str, action='store', dest='fmt',
                   default="ace",
                   help='set the output format, one of {ace, csv, html} (default: ace)')

parser.add_argument('-o', '--out', type=str, action='store', dest='out', default="dir_in",
                   help='set the directory where the output files are stored (default: same as "in")')

parser.add_argument('-v', '--version', action='version', version='%(prog)s v0.1')

args = parser.parse_args()

# TODO: there is probably a better way to do this
if args.dir_in is None:
	print >> sys.stderr, 'ERROR: argument -i/--in is not specified'
	exit()

print >> sys.stderr, 'TODO: fmt:', args.fmt
print >> sys.stderr, 'TODO: out:', args.out

g = owl_file_generator(args.dir_in)

server = None
time_start = None

if args.mode == 'http':
	print 'Starting the server'
	cmd = [owl_to_ace_exe, '-httpserver', '-port', str(port)]
	print cmd
	server = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	wait_until_up(server)
	time_start = time.time()
	post_files_with_curl(g)
else:
	time_start = time.time()
	run_as_script(g)


while threading.active_count() > 1:
	print '{:} threads still active'.format(threading.active_count())
	time.sleep(.2)

time_end = time.time()

# Stop the verbalization server in case it was started
if server is not None:
	print 'Stopping the server'
	server.terminate()

print 'Duration: {:.2f} sec'.format(time_end - time_start)
