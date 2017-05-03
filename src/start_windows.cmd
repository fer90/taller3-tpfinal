@ECHO OFF

start /b matlab -nojvm -nosplash -nodesktop -r 'matlab.engine.shareEngine'

python main.py