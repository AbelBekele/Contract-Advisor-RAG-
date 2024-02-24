import { useEffect, useState } from 'react';
import userService from '@/api/user';
import toast from 'react-hot-toast';

const CODE_SECONDS = 60;

const useMobileCode = () => {
  let timer = 0;
  const [time, setTime] = useState(0);

  useEffect(() => {
    if (time === CODE_SECONDS) timer = setInterval(() => setTime((time) => --time), 1000);
    else if (time <= 0) timer && clearInterval(timer);
  }, [time]);

  const handleGetCode = async (phoneNumber: string) => {
    if (!/^(?:(?:\+|00)86)?1\d{10}$/.test(phoneNumber)) {
      toast.error('Wrong mobile number');
      return;
    }

    try {
      await userService.getPhoneCode(phoneNumber);
      setTime(CODE_SECONDS);
    } catch (e) {
      toast.error(e as string);
    }
  };
  return {
    time,
    handleGetCode,
  };
};

export default useMobileCode;
