// const baseURL = `http://172.20.10.3:8000`
const baseURL = `http://localhost:8000`;

type PaymentResponse = {
  data: string;
  money: string;
};

const Payment = async (user: string): Promise<PaymentResponse | string> => {
  const response = await fetch(`${baseURL}/payment/` + user, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Origin: "http://localhost:8000",
    },
  });

  if(user) {
    const { data, money } = await response.json();
    return { data: data, money: money };
  } else {
    const { data } = await response.json();
    return data;
  }
};

export { Payment };
