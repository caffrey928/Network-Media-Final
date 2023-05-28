const base64url = {
    encode: (buf) => {
        const base64 = btoa(String.fromCharCode(...buf));
        return base64.replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
    },
    decode: (str) => {
        str = str.replace(/-/g, '+').replace(/_/g, '/');
        while (str.length % 4) {
            str += '=';
        }
        const array = new Uint8Array(atob(str).split('').map((char) => char.charCodeAt(0)));
        return array;
    },
}

export async function Registration(Username: string){

    let response = await getallUsers();
    let Users = response.Users
    console.log(Users)
    // let Username = document.getElementById('username').value;

    if (Username === "") {
        window.alert("Please type a Username!");
        return
    }

    //確認使用者是否存在
    for (var i = 0; i <= Users.length - 1; i++) {
        if (Users[i].name === Username){
            alert("User already exist!")
            return
        }
    }

    //創建一組新的userID
    var userID = makeid(20)

    //創建挑戰（實務上應由後端創建會較保險）
    var challenge = new Uint8Array(32);
    window.crypto.getRandomValues(challenge);

    
    console.log(challenge)
    console.log(userID)


    //創建publicKey物件（投影片p9）
    var publicKey = {
        //TODO:完成publicKey物件（20分）
        challenge: challenge,
        rp: {
            name: "Localhost Inc.",
            id: "localhost",
        },
        user: {
            id: Uint8Array.from(
                userID, c => c.charCodeAt(0)),
            name: Username,
            displayName: Username,
        },
        pubKeyCredParams: [{alg: -7, type: "public-key"}],
        authenticatorSelection: {
            // authenticatorAttachment: "cross-platform",
            requireResidentKey: true,
        },
        timeout: 60000,
        attestation: "direct"
    }

    //發起註冊程序
    navigator.credentials.create({ 'publicKey': publicKey })
    .then((newCredentialInfo) => {
        console.log('SUCCESS', newCredentialInfo)

        const decodedAttestationObj = CBOR.decode(newCredentialInfo.response.attestationObject);
        console.log(decodedAttestationObj)

        //TODO:
        //    從decodedAttestationObj中拆解credentialId（bytearray形式）（5分）
        //    從decodedAttestationObj中拆解出publicKeyObject（投影片p21、p22）（10分）
        //    驗證挑戰是否相符（10
        const {authData} = decodedAttestationObj;
        const dataView = new DataView(new ArrayBuffer(2));
        const idLenBytes = authData.slice(53, 55);
        idLenBytes.forEach((value, index) => dataView.setUint8(index, value));
        const credentialIdLength = dataView.getUint16(); 
        const credentialId = authData.slice(55, 55 + credentialIdLength);
        const publicKeyBytes = authData.slice(55 + credentialIdLength);
        const publicKeyObject = CBOR.decode(publicKeyBytes.buffer);
        console.log(credentialId)
        console.log(publicKeyObject)

        clientDataJSON = newCredentialInfo.response.clientDataJSON
        clientDataJSON_string = new TextDecoder("utf-8").decode(clientDataJSON)
        clientDataJSON_JSON = JSON.parse(clientDataJSON_string)
        console.log(clientDataJSON_JSON)

        if (clientDataJSON_JSON.challenge !== base64url.encode(challenge)) {
            window.alert("Fail to pass challenge!");
            return
        }

        storeUser(Username, base64url.encode(credentialId), publicKeyObject)

        alert("Registration Successful!")
    })
    .catch((error) => {
        console.log('FAIL', error)
    })


    


}

export async function Login(Username: string){
    let response = await getallUsers();
    let Users = response.Users
    // let Username = document.getElementById('username').value;
    console.log(Users)
    if (Username === "") {
        window.alert("Please type a Username!");
        return
    }
    console.log(Users.length)
    let match = false

    //從所有使用者中一一比對
    for (var i = 0; i <= Users.length - 1; i++) {
        if (Users[i].name === Username){
            match = true

            //創建驗證用的挑戰            
            var challenge = new Uint8Array(32);
            window.crypto.getRandomValues(challenge);
            console.log(base64url.encode(challenge))

            const publicKeyCredentialRequestOptions = {
                //TODO:完成publicKeyCredentialRequestOptions（10分）
                //註：若想使用手機的Passkey，最好直接不要specify "transport"這個選項，也就是直接不要加
                challenge: challenge,
                allowCredentials: [{
                    id: base64url.decode(Users[i].id),
                    type: 'public-key',
                }],
                timeout: 60000,
            }

            navigator.credentials.get({publicKey: publicKeyCredentialRequestOptions})
            .then((assertion) => {
                console.log(assertion)

                //TODO:驗證挑戰是否相符（15分）
                clientDataJSON = assertion.response.clientDataJSON
                clientDataJSON_string = new TextDecoder("utf-8").decode(clientDataJSON)
                clientDataJSON_JSON = JSON.parse(clientDataJSON_string)
                console.log(clientDataJSON_JSON)

                if (clientDataJSON_JSON.challenge !== base64url.encode(challenge)) {
                    window.alert("Fail to pass challenge!");
                    return
                }

                authUser(Username, assertion.response.clientDataJSON, assertion.response.authenticatorData, assertion.response.signature)
                .then((result) => {
                    console.log(result)
                    if (result) {
                        alert("Successfully login!")
                        document.getElementById('main').style.display = "none"
                        document.getElementById('dog').style.display = "inline-block"
                        return
                    }else{
                        alert("login failed!")
                    }
                })
            })
            .catch((error) => {
                location.reload()
                console.log('FAIL', error)
            })


        }
    }

    if(!match) alert("User doesn't exist!")
}


function makeid(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
}


async function getallUsers(){
    try {
        const response = await fetch('http://localhost:8000/UserDB/', {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Origin': 'http://localhost:8000'
            }
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}


async function storeUser(name, id, publicKey){
    try {
        const response = await fetch("http://localhost:8000/UserDB/" + name, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Origin': 'http://localhost:8000'
            },
            body: JSON.stringify({
                name: name,
                id: id,
                publicKey: publicKey
            })
        })
        if (response.status === 403) {
            alert("User already exist!")
        }
    } catch (error) {

        console.error(error);
    }
}

async function authUser(name, clientData, authData, signature){
    try {
        const response = await fetch("http://localhost:8000/Auth/" + name, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Origin': 'http://localhost:8000'
            },
            body: JSON.stringify({
                name: name,
                clientData: new Uint8Array(clientData),
                authData: new Uint8Array(authData),
                signature: new Uint8Array(signature)

            })
        })
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
    }
}