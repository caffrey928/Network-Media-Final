import { useState, CSSProperties } from "react";
import "./App.css";
import { Login, Registration } from "./util/login_register";
import { Payment } from "./util/payment";
import background from "./assets/background.jpg";
import BarLoader from "react-spinners/BarLoader";

function App() {
  const [Username, setUsername] = useState("");
  const [loginUser, setLoginUser] = useState("");
  const [payStatus, setPayStatus] = useState("No Payment!");
  const [money, setMoney] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(e: React.ChangeEvent<HTMLInputElement>): void {
    setUsername(e.target.value);
  }

  async function handlePayment(): Promise<void> {
    try {
      setLoading(true);
      const response = await Payment(loginUser);
      setLoading(false);

      if (typeof response === "string") setPayStatus(response);
      else {
        setPayStatus(response.data);
        setMoney(response.money);
      }
    } catch (error) {
      console.log(error);
      alert("Some Error Occured!");
      setLoading(false);
    }
  }

  const handleRegistration = (): void => {
    try{
      Registration(Username);
    } catch (error){
      console.log(error);
      alert("Some Error Occured!");
    }
    
  }

  async function handleLogin(): Promise<void> {
    try {
      const response = await Login(Username);

      if (response) {
        console.log("Login Success");
        setLoginUser(Username);
        setMoney(response);
      }
    } catch (error) {
      console.log(error);
      alert("Some Error Occured!");
    }
  }

  const handleSignOut = (): void => {
    setLoginUser("");
    setMoney("");
    setUsername("");
  };

  const override: CSSProperties = {
    // display: "in-line",
    margin: "0 auto",
    borderColor: "white",
  };

  const Loader = () => {
    return (
      <>
        <p
          style={{
            fontSize: "20px",
            textAlign: "center",
            marginBottom: "1rem",
          }}
        >
          Dealing Payment...
        </p>
        <BarLoader
          color="white"
          loading={loading}
          height={8}
          width={200}
          cssOverride={override}
        />
      </>
    );
  };

  return (
    <>
      <div className="page">
        <img
          src={background}
          alt="background image"
          className="background__img"
        />

        <div className="dialog__form">
          <h1 className="dialog__title">IOTA Vending Machine</h1>
          <p className="dialog__text">Payment Status: {payStatus}</p>
          {loginUser ? (
            <>
              <p className="dialog__text">User: {loginUser}</p>
              <p className="dialog__text">account balance: {money}</p>
              <button
                className="dialog__button"
                onClick={() => handleSignOut()}
              >
                Sign Out
              </button>
            </>
          ) : (
            <>
              <div className="dialog__box">
                <i className="ri-user-3-line dialog__origin__icon"></i>

                <div className="dialog__box-input">
                  <input
                    type="text"
                    className="dialog__input"
                    placeholder=" "
                    value={Username}
                    onChange={handleChange}
                  />
                  <label htmlFor="" className="dialog__label">
                    Username
                  </label>
                </div>
              </div>
              <div className="grid-container-login-reg">
                <button
                  className="dialog__button grid-item"
                  style={{ width: "80%" }}
                  onClick={() => handleLogin()}
                >
                  Login
                </button>
                <button
                  className="dialog__button grid-item"
                  style={{ width: "80%" }}
                  onClick={() => handleRegistration()}
                >
                  Register
                </button>
              </div>
            </>
          )}

          {loading ? (
            <Loader />
          ) : (
            <button className="dialog__button" onClick={() => handlePayment()}>
              Apply Payment
            </button>
          )}

          {/* <div className="grid-container">
                        <div />
                        <h1 className="dialog__title">{tutorial ? "Tutorial" : "Verifier"}</h1>
                        <div className="dialog__iconbutton">
                            <IconButton size="large" title="Tutorial" onClick={() => setTutorial(!tutorial)}>
                                {tutorial ? <CloseIcon className="dialog__icon" /> : <ErrorOutlineIcon className="dialog__icon" />}
                            </IconButton>
                        </div>
                    </div>
                    {tutorial ? <TutorialPage /> : <MainPage />} */}
        </div>
      </div>
    </>
    // <>
    //     <input type="text" value={Username} onChange={handleChange} />
    //   <h1>{loginUser ? loginUser : "HiHi"}</h1>
    //   <h1>{loginUser ? money : "not yet login!"}</h1>
    // </>
  );
}

export default App;
