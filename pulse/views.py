from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login , logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from web3 import Web3
from django.views.decorators.csrf import csrf_exempt
import requests
from web3 import Web3
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


current_data = {"pulse": 0, "oxygen": 0}
ESP32_IP = "http://10.191.215.152/"

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"  # Update with your Ganache URL
web3 = Web3(Web3.HTTPProvider(ganache_url))
# Check connection
assert web3.is_connected(), "Failed to connect to Ganache"
# Contract details
contract_address = "0x20c07f2B44115E9671722cF23940A51c24A36A64"  # Replace with your deployed contract address
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "userId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "heartRate",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "oxygenLevel",
				"type": "uint256"
			}
		],
		"name": "addHealthData",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "userId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "heartRate",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "oxygenLevel",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "HealthDataAdded",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "userId",
				"type": "uint256"
			}
		],
		"name": "getHealthData",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "timestamp",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "heartRate",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "oxygenLevel",
						"type": "uint256"
					}
				],
				"internalType": "struct HealthData.HealthEntry[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
] # Paste the contract ABI here

contract = web3.eth.contract(address=contract_address, abi=contract_abi)



def main(request):
    return render(request,"pulse/main.html")

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login")) 
    return render(request, "logged")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('logged'), {'user': request.user})
        else:
            return render(request,"pulse/userlogin2.html")
    return render(request,"pulse/userlogin.html")


def logged(request):
    return render(request, 'pulse/logged.html')

def latest(request,user_id):
    if request.user.id != user_id:
        return HttpResponseForbidden("You are not allowed to access this page.<br><a href='http://127.0.0.1:8000/pulse/login'>Go back to login</a>.")
    return render(request, 'pulse/latest.html', {
        'user_id':user_id,
        'pulse_rate': current_data["pulse"],
        'blood_oxygen': current_data["oxygen"]
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@csrf_exempt
def get_realtime_data(request):
    try:
        # Fetch data from ESP32 API
        response = requests.get(ESP32_IP)
        if response.status_code == 200:
            data = response.json()  # Retrieve JSON data
            # Update the current data dictionary
            current_data["pulse"] = data.get("pulse_rate", 0)
            current_data["oxygen"] = data.get("blood_oxygen", 0)
            return JsonResponse(data)  # Send data back to frontend as JSON
        else:
            return JsonResponse({"error": "Failed to fetch data from ESP32"}, status=500)
    except requests.ConnectionError:
        return JsonResponse({"error": "ESP32 connection error"}, status=500)


def proxy_esp32_data(request):
    esp32_url = "http://10.191.215.152/"
    try:
        response = requests.get(esp32_url)
        data = response.json()  # Convert the ESP32 JSON response to a Python dictionary
    except requests.RequestException as e:
        data = {"error": "Failed to fetch data from ESP32", "details": str(e)}
    return JsonResponse(data)



def add_health_data(user_id, heart_rate, oxygen_level):
    tx_hash = contract.functions.addHealthData(user_id, heart_rate, oxygen_level).transact({
        'from': web3.eth.accounts[0]  # Replace with the sender's address
    })
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return "Health data added successfully!"

def get_health_data(user_id):
    return contract.functions.getHealthData(user_id).call()


# New function to handle the input form and display
def input_health_data(request):
    if request.method == "POST":
        # Get form data from the POST request
        user_id = int(request.POST.get("user_id"))
        heart_rate = int(request.POST.get("heart_rate"))
        oxygen_level = int(request.POST.get("oxygen_level"))

         # Send the data to the blockchain
        tx_hash = contract.functions.addHealthData(user_id, heart_rate, oxygen_level).transact({
                'from': web3.eth.accounts[0]
            })
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return render(request, "pulse/input_health_data.html")


    return render(request, "pulse/input_health_data.html")


def input_health_data_2(request ):
    
    if request.method == "POST":
		# Get form data from the POST request
        user_id = int(request.POST.get("user_id"))
        heart_rate = int(request.POST.get("heart_rate"))
        oxygen_level = int(request.POST.get("oxygen_level"))

         # Send the data to the blockchain
        tx_hash = contract.functions.addHealthData(user_id, heart_rate, oxygen_level).transact({
                'from': web3.eth.accounts[0]
            })
        web3.eth.wait_for_transaction_receipt(tx_hash)		
        return redirect('latest',user_id)


    return redirect('latest',user_id)
    

@login_required
def show_user_data(request, user_id):
    if request.user.id != user_id:
        return HttpResponseForbidden("You are not allowed to access this page.<br><a href='http://127.0.0.1:8000/pulse/login'>Go back to login</a>.")
    # Fetch the health data from blockchain for this user
    health_d = get_health_data(user_id)
    health_data = sorted(health_d, key=lambda x: x[0], reverse=True)
    # Return the data to the template
    return render(request, 'pulse/show_user_data.html', {'health_data': health_data, 'user_id': user_id})




