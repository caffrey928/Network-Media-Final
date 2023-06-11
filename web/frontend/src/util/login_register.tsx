import { decode } from "./CBOR";

const base64url = {
  encode: (buf: Uint8Array) => {
    const base64 = btoa(String.fromCharCode(...buf));
    return base64.replace(/=/g, "").replace(/\+/g, "-").replace(/\//g, "_");
  },
  decode: (str: string) => {
    str = str.replace(/-/g, "+").replace(/_/g, "/");
    while (str.length % 4) {
      str += "=";
    }
    const array = new Uint8Array(
      atob(str)
        .split("")
        .map((char) => char.charCodeAt(0))
    );
    return array;
  },
};

export async function Registration(Username: string): Promise<void> {
  const response = await getallUsers();
  const Users = response.Users;
  console.log(Users);

  if (Username === "") {
    window.alert("Please type a Username!");
    return;
  }

  // check if user exists
  for (var i = 0; i <= Users.length - 1; i++) {
    if (Users[i].name === Username) {
      alert("User already exist!");
      return;
    }
  }

  // create new userID
  const userID = makeid(20);

  // create challenge
  const challenge = new Uint8Array(32);
  window.crypto.getRandomValues(challenge);

  console.log(challenge);
  console.log(userID);

  // create publicKey
  const publicKey: PublicKeyCredentialCreationOptions = {
    challenge: challenge,
    rp: {
      name: "Localhost Inc.",
      id: "localhost",
    },
    user: {
      id: Uint8Array.from(userID, (c) => c.charCodeAt(0)),
      name: Username,
      displayName: Username,
    },
    pubKeyCredParams: [{ alg: -7, type: "public-key" }],
    authenticatorSelection: {
      // authenticatorAttachment: "cross-platform",
      requireResidentKey: true,
    },
    timeout: 60000,
    attestation: "direct",
  };

  // register process
  navigator.credentials
    .create({ publicKey: publicKey })
    .then((newCredentialInfo) => {
      if (!newCredentialInfo) throw new Error("No credentialInfo returned");
      console.log("SUCCESS", newCredentialInfo);

      const decodedAttestationObj = decode(
        (
          (newCredentialInfo as PublicKeyCredential)
            .response as AuthenticatorAttestationResponse
        ).attestationObject,
        "tagger",
        "simple"
      );
      // console.log(decodedAttestationObj)

      const { authData } = decodedAttestationObj;
      const dataView = new DataView(new ArrayBuffer(2));
      const idLenBytes = authData.slice(53, 55);
      idLenBytes.forEach((value: number, index: number) =>
        dataView.setUint8(index, value)
      );
      const credentialIdLength = dataView.getUint16(0);
      const credentialId = authData.slice(55, 55 + credentialIdLength);
      const publicKeyBytes = authData.slice(55 + credentialIdLength);
      const publicKeyObject = decode(publicKeyBytes.buffer, "tagger", "simple");

      const clientDataJSON = (newCredentialInfo as PublicKeyCredential).response
        .clientDataJSON;
      const clientDataJSON_string = new TextDecoder("utf-8").decode(
        clientDataJSON
      );

      const clientDataJSON_JSON = JSON.parse(clientDataJSON_string);

      if (clientDataJSON_JSON.challenge !== base64url.encode(challenge)) {
        window.alert("Fail to pass challenge!");
        return;
      }

      storeUser(Username, base64url.encode(credentialId), publicKeyObject);

      alert("Registration Successful!");
    })
    .catch((error) => {
      console.log("FAIL", error);
    });
}

export const Login = async (Username: string): Promise<string> => {
  let response = await getallUsers();
  let Users = response.Users;
  console.log(Users);
  if (Username === "") {
    window.alert("Please type a Username!");
    return "";
  }
  console.log(Users.length);
  let match = false;
  let login = "";

  // compare all users one by one
  for (var i = 0; i <= Users.length - 1; i++) {
    if (Users[i].name === Username) {
      match = true;

      // create challenge for verify
      var challenge = new Uint8Array(32);
      window.crypto.getRandomValues(challenge);
      console.log(base64url.encode(challenge));

      const publicKeyCredentialRequestOptions: PublicKeyCredentialRequestOptions =
        {
          challenge: challenge,
          allowCredentials: [
            {
              id: base64url.decode(Users[i].id),
              type: "public-key",
            },
          ],
          timeout: 60000,
        };

      await navigator.credentials
        .get({ publicKey: publicKeyCredentialRequestOptions })
        .then(async (assertion) => {
          if (!assertion) throw new Error("No assertion returned");
          console.log(assertion);

          // check challenge
          let clientDataJSON = (assertion as PublicKeyCredential).response
            .clientDataJSON;
          let clientDataJSON_string = new TextDecoder("utf-8").decode(
            clientDataJSON
          );
          let clientDataJSON_JSON = JSON.parse(clientDataJSON_string);
          console.log(clientDataJSON_JSON);

          if (clientDataJSON_JSON.challenge !== base64url.encode(challenge)) {
            window.alert("Fail to pass challenge!");
            return "";
          }

          await authUser(
            Username,
            (assertion as PublicKeyCredential).response.clientDataJSON,
            (
              (assertion as PublicKeyCredential)
                .response as AuthenticatorAssertionResponse
            ).authenticatorData,
            (
              (assertion as PublicKeyCredential)
                .response as AuthenticatorAssertionResponse
            ).signature
          ).then((result: string) => {
            if (result !== "Fail to login!") {
              alert("Successfully login!");
              login = result;
            } else {
              alert("Login Failed!");
            }
          });
        })
        .catch((error) => {
          location.reload();
          console.log("FAIL", error);
          return "";
        });
    }
  }

  if (!match) alert("User doesn't exist!");

  if (login !== "") return login;
  else return "";
};

function makeid(length: number): string {
  let result = "";
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const charactersLength = characters.length;

  let counter = 0;
  while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
  }

  return result;
}

async function getallUsers() {
  try {
    const response = await fetch("http://localhost:8000/UserDB/", {
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Origin: "http://localhost:8000",
      },
    });
    const data = await response.json();

    return data;
  } catch (error) {
    console.error(error);
  }
}

async function storeUser(
  name: string,
  id: string,
  publicKey: object
): Promise<void> {
  try {
    const response = await fetch("http://localhost:8000/UserDB/" + name, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Origin: "http://localhost:8000",
      },
      body: JSON.stringify({
        name: name,
        id: id,
        publicKey: publicKey,
        money: 0,
      }),
    });
    if (response.status === 403) {
      alert("User already exist!");
    }
  } catch (error) {
    console.error(error);
  }
}

async function authUser(
  name: string,
  clientData: ArrayBuffer,
  authData: ArrayBuffer,
  signature: ArrayBuffer
): Promise<string> {
  try {
    const response = await fetch("http://localhost:8000/Auth/" + name, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Origin: "http://localhost:8000",
      },
      body: JSON.stringify({
        name: name,
        clientData: new Uint8Array(clientData),
        authData: new Uint8Array(authData),
        signature: new Uint8Array(signature),
      }),
    });
    const { status, data } = await response.json();

    if (status) return data;
    else return "Fail to login!";
  } catch (error) {
    console.error(error);
    return "";
  }
}
