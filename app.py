import json

import ProductionPlanEngine.ProductionPlanEngine as ppe
import ProductionPlanEngine.Verifyer as verifyer

from flask import Flask, request
app = Flask(__name__)

@app.route('/productionplan', methods=['POST'])
def productionplan():
    try:
        payload = json.loads(request.data)
        payload = verifyer.verifyPayload(payload)

        responce = ppe.calculateProductionPlan(**payload)
        code = 200
    except Exception as e:
        responce = { "Error": str(e) }
        code = 400

    return json.dumps(responce), code

if __name__ == '__main__':
    app.run(port=8888, debug=True)
