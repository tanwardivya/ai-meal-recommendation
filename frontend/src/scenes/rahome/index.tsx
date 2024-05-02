import { Box } from "@mui/material";
import HomeNavBar from "@/scenes/homenavbar";
import Chat from "@/scenes/chat";
type Props = {};

const RAHomePage = ({}: Props) => {
  return (
    <Box>
      <HomeNavBar />
      <Chat />
    </Box>
  );
};

export default RAHomePage;
