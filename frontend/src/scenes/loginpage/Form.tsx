// eslint-disable-next-line @typescript-eslint/ban-ts-comment
//@ts-nocheck
import { useState } from "react";
import {
  Box,
  Button,
  TextField,
  useMediaQuery,
  Typography,
  useTheme,
} from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { setLogin } from "@/state";

interface LoginValues {
  email: string;
  password: string;
}

const initialValuesLogin: LoginValues = {
  email: "",
  password: "",
};

interface RegisterValues extends LoginValues {
  firstname: string;
  lastname: string;
  location: string;
  dietary_preference: string;
}

const initialValuesRegister: RegisterValues = {
  firstname: "",
  lastname: "",
  email: "",
  password: "",
  location: "",
  dietary_preference: "",
};

const registerSchema: yup.Schema<RegisterValues> = yup.object().shape({
  firstname: yup.string().required("required"),
  lastname: yup.string().required("required"),
  email: yup.string().email("invalid email").required("required"),
  password: yup.string().required("required"),
  location: yup.string().required("required"),
  dietary_preference: yup.string().required("required"),
});

const loginSchema: yup.Schema<LoginValues> = yup.object().shape({
  email: yup.string().email("invalid email").required("required"),
  password: yup.string().required("required"),
});

interface SubmitProps {
  resetForm: () => void;
}

type FormValues = LoginValues | RegisterValues;
const serverBaseURL =
  "https://recipe-agent-app.greenmeadow-35e3d21d.westus3.azurecontainerapps.io";
function getInitialValues(isLogin: boolean): FormValues {
  return isLogin
    ? (initialValuesLogin as LoginValues)
    : (initialValuesRegister as RegisterValues);
}

const Form = () => {
  const [pageType, setPageType] = useState("login");
  const { palette } = useTheme();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const isNonMobile = useMediaQuery("(min-width:600px)");
  const isLogin = pageType === "login";
  const isRegister = pageType === "register";
  const register = async (
    values: RegisterValues,
    onSubmitProps: SubmitProps,
  ) => {
    // this allows us to send form info with image
    const formData = new FormData();
    //@ts-no-check
    for (let key in values) {
      const value = values[key as keyof RegisterValues];
      formData.append(key, String(value));
    }

    const savedUserResponse = await fetch(
      "http://localhost:8000/users/register",
      {
        method: "POST",
        body: formData,
      },
    );
    const savedUser = await savedUserResponse.json();
    onSubmitProps.resetForm();

    if (savedUser) {
      setPageType("login");
    }
  };
  const login = async (values: LoginValues, onSubmitProps: SubmitProps) => {
    const loggedInResponse = await fetch("http://localhost:8000/users/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });
    const loggedIn = await loggedInResponse.json();
    onSubmitProps.resetForm();
    if (loggedIn) {
      dispatch(
        setLogin({
          user: loggedIn.user,
          token: loggedIn.token,
        }),
      );
      navigate("/home");
    }
  };
  const handleFormSubmit = async (
    values: FormValues,
    onSubmitProps: SubmitProps,
  ) => {
    if (isLogin) await login(values as LoginValues, onSubmitProps);
    if (isRegister) await register(values as RegisterValues, onSubmitProps);
  };

  return (
    <Formik
      onSubmit={handleFormSubmit}
      initialValues={getInitialValues(isLogin)}
      validationSchema={isLogin ? loginSchema : registerSchema}
    >
      {({
        values,
        errors,
        touched,
        handleBlur,
        handleChange,
        handleSubmit,
        resetForm,
      }) => (
        <form onSubmit={handleSubmit}>
          <Box
            display="grid"
            gap="30px"
            gridTemplateColumns="repeat(4, minmax(0, 1fr))"
            sx={{
              "& > div": { gridColumn: isNonMobile ? undefined : "span 4" },
            }}
          >
            {isRegister && (
              <>
                <TextField
                  label="First Name"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  value={values.firstname}
                  name="firstname"
                  error={
                    Boolean(touched.firstname) && Boolean(errors.firstname)
                  }
                  helperText={touched.firstname && errors.firstname}
                  sx={{ gridColumn: "span 2" }}
                />
                <TextField
                  label="Last Name"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  value={values.lastname}
                  name="lastname"
                  error={Boolean(touched.lastname) && Boolean(errors.lastname)}
                  helperText={touched.lastname && errors.lastname}
                  sx={{ gridColumn: "span 2" }}
                />
                <TextField
                  label="Location"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  value={values.location}
                  name="location"
                  error={Boolean(touched.location) && Boolean(errors.location)}
                  helperText={touched.location && errors.location}
                  sx={{ gridColumn: "span 4" }}
                />
                <TextField
                  label="Dietary Preference"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  value={values.dietary_preference}
                  name="dietary_preference"
                  error={
                    Boolean(touched.dietary_preference) &&
                    Boolean(errors.dietary_preference)
                  }
                  helperText={
                    touched.dietary_preference && errors.dietary_preference
                  }
                  sx={{ gridColumn: "span 4" }}
                />
              </>
            )}

            <TextField
              label="Email"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.email}
              name="email"
              error={Boolean(touched.email) && Boolean(errors.email)}
              helperText={touched.email && errors.email}
              sx={{ gridColumn: "span 4" }}
            />
            <TextField
              label="Password"
              type="password"
              onBlur={handleBlur}
              onChange={handleChange}
              value={values.password}
              name="password"
              error={Boolean(touched.password) && Boolean(errors.password)}
              helperText={touched.password && errors.password}
              sx={{ gridColumn: "span 4" }}
            />
          </Box>

          {/* BUTTONS */}
          <Box>
            <Button
              fullWidth
              type="submit"
              sx={{
                m: "2rem 0",
                p: "1rem",
                backgroundColor: palette.primary.main,
                color: palette.background.paper,
                "&:hover": { color: palette.primary.main },
              }}
            >
              {isLogin ? "LOGIN" : "REGISTER"}
            </Button>
            <Typography
              onClick={() => {
                setPageType(isLogin ? "register" : "login");
                resetForm();
              }}
              sx={{
                textDecoration: "underline",
                color: palette.primary.main,
                "&:hover": {
                  cursor: "pointer",
                  color: palette.primary.light,
                },
              }}
            >
              {isLogin
                ? "Don't have an account? Sign Up here."
                : "Already have an account? Login here."}
            </Typography>
          </Box>
        </form>
      )}
    </Formik>
  );
};

export default Form;
