import axios from "axios";

const baseURL = `http://172.20.10.3:8000`

// type PaymentResponse = {
//       payment: string
// }

const Payment = async () => {
  const { data } = await axios.get<string>(`${baseURL}/payment`);
  // console.log(data)
  
  return data;
}

export { Payment }
