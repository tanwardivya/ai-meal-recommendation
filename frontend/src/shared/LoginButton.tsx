import React from "react";
import { useNavigate } from "react-router-dom";

type Props = {
  children: React.ReactNode;
};

const LoginButton = ({ children }: Props) => {
    const navigate = useNavigate();
  
    const handleClick = () => {
      navigate('/login'); // Navigate to /login when the button is clicked
    };
  
    return (
      <button
        className="rounded-md bg-secondary-500 px-10 py-2 hover:bg-primary-500 hover:text-white"
        onClick={handleClick}
      >
        {children}
      </button>
    );
  };

export default LoginButton;