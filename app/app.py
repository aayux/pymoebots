from flask import Flask, render_template, request, url_for, send_file
import random

app = Flask(__name__)


def tempFunction(dataDict):
  directions = [{'x': -1, 'y': 1}, {'x': 0, 'y': 1}, {'x': 1, 'y': 0}, {'x': 1, 'y': -1}, {'x': 0, 'y': -1}, {'x': -1, 'y': 0}]
  print('\033[92m' + 'Client requests: ' + dataDict['algName'])

  if dataDict['leader'] < 0:
    dataDict['leader'] = random.randint(0, len(dataDict['amoebotsPos']) - 1)

  for amoebot in dataDict['amoebotsPos']:
    print('\033[94m\t', amoebot)

  for i in range(len(dataDict['amoebotsPos'])):
    head = dataDict['amoebotsPos'][i]['head']
    tail = dataDict['amoebotsPos'][i]['tail']
    if (head['x'] != tail['x']) or (head['y'] != tail['y']):
      tail['x'] = head['x']
      tail['y'] = head['y']
    else:
      direction = directions[random.randint(0, 5)]
      head['x'] += direction['x']
      head['y'] += direction['y']

  print('\033[92m' + 'Responding:')
  for amoebot in dataDict['amoebotsPos']:
    print('\033[94m\t', amoebot)

  print('\033[00m')
  return dataDict


@app.route('/')
def main():
  return render_template('main.html')

@app.route('/word', methods=['POST'])
def word():
  if request.method == 'POST':
    data = request.get_json()
    newData = tempFunction(data)
    return newData
  print('\033[91mWarning: someone tried to GET something\033[00m')

@app.route('/history', methods=['GET'])
def history():
  if request.method == 'GET':
    with open ('app/static/full_history.json', "r") as data:
      print(data)
    return send_file('static/full_history.json', attachment_filename='history.json'), 200

if __name__ == '__main__':
  app.run(debug=True, port=6000)
















