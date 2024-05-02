import { Box, Typography, useTheme, useMediaQuery } from "@mui/material";
import Form from "./Form"
type Props = object;

// eslint-disable-next-line no-empty-pattern
const Login = ({}: Props) => {
  const theme = useTheme();
  const isNonMobileScreens = useMediaQuery("(min-width: 1000px)");
  return (
    <Box>
      <Box
        width="100%"
        sx={{
          backgroundColor: theme.palette.background.paper,
          p: "1rem 6%",
          textAlign: "center",
        }}
      >
        {" "}
        <Typography fontWeight="bold" fontSize="32px" color="primary">
          Recipe Assistant
        </Typography>
      </Box>
      <Box
        width={isNonMobileScreens ? "50%" : "93%"}
        sx={{
          backgroundColor: theme.palette.background.paper,
          p: "2rem",
          m: "2rem auto",
          borderRadius: "1.5rem",
        }}
      >
       <Typography fontWeight="500" variant="h5" sx={{ mb: "1.5rem" }}>
          Welcome to Recpie Assistant, Your Personalized Culinary Navigator!
       </Typography>
       <Form/>
      </Box>
    </Box>
  );
};

export default Login;
