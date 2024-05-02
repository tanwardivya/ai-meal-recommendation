import { useRef, useState } from "react";
import {
  Box,
  Avatar,
  Typography,
  useTheme,
  Button,
  IconButton,
} from "@mui/material";
import red from "@mui/material/colors/red";
import { RootState } from "@/redux";
import { useSelector } from "react-redux";
import ChatItem from "@/shared/ChatItem";
import { IoMdSend } from "react-icons/io";
import { sendChatRequest, deleteChatRequest } from "@/helpers/api-communicator";
import toast from "react-hot-toast";

type Message = {
  role: "user" | "assistant";
  content: string;
};
// const serverBaseURL = "http://localhost:8000";
const Chat = () => {
  const user = useSelector((state: RootState) => state.user);
  const token = useSelector((state: RootState) => state.token);
  const { palette } = useTheme();
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [chatMessages, setChatMessages] = useState<Message[]>([]);

  const handleSubmit = async () => {
    const content = inputRef.current?.value as string;
    if (inputRef && inputRef.current) {
      inputRef.current.value = "";
    }
    const newMessage: Message = { role: "user", content };
    setChatMessages((prev) => [...prev, newMessage]);
    //@ts-expect-error ignore type
    const chatData = await sendChatRequest(content, token);
    // setChatMessages((prev) => [...prev, ...chatData.chats]);
    setChatMessages((prev) => {
      // Create a set of messages based on unique identifiers or contents to prevent duplicates
      const existingMessages = new Set(prev.map((msg) => JSON.stringify(msg)));
      const filteredNewMessages = chatData.chats.filter(
        (msg) => !existingMessages.has(JSON.stringify(msg)),
      );
      return [...prev, ...filteredNewMessages];
    });
  };

  const handleDeleteChats = async () => {
    toast.loading("Deleting Chats", { id: "deletechats" });
    //@ts-expect-error ignore type
    await deleteChatRequest(token);
    setChatMessages([]);
    toast.success("Deleted Chats Successfully", { id: "deletechats" });
  };
  return (
    <Box
      sx={{
        display: "flex",
        flex: 1,
        width: "100%",
        height: "100%",
        mt: 3,
        gap: 3,
      }}
    >
      <Box
        sx={{
          display: { md: "flex", xs: "none", sm: "none" },
          flex: 0.2,
          flexDirection: "column",
        }}
      >
        <Box
          sx={{
            display: "flex",
            width: "100%",
            height: "60vh",
            bgcolor: "rgb(17,29,39)",
            borderRadius: 5,
            flexDirection: "column",
            mx: 3,
          }}
        >
          <Avatar
            sx={{
              mx: "auto",
              my: 2,
              bgcolor: "white",
              color: "black",
              fontWeight: 700,
            }}
          >
            {user?.firstname[0]}
            {user?.lastname[0]}
          </Avatar>
          <Typography
            sx={{
              mx: "auto",
              fontFamily: "sans-serif",
              color: palette.primary.main,
            }}
          >
            Welcome to Recipe Assistant
          </Typography>
          <Typography
            sx={{
              mx: "auto",
              fontFamily: "sans-serif",
              my: 4,
              p: 3,
              color: palette.primary.main,
            }}
          >
            Whether you're looking for vegan/vegetarian/non-vegetarian delights,
            I'm here to help and discover healthy recipes tailored to your
            dietary preferences. Simply tell me what you're in the mood for, and
            I'll handle the rest, ensuring you can enjoy delicious and
            nutritious meals that fit your lifestyle perfectly.
          </Typography>
          <Button
            onClick={handleDeleteChats}
            sx={{
              width: "200px",
              my: "auto",
              color: "white",
              fontWeight: "700",
              borderRadius: 3,
              mx: "auto",
              bgcolor: red[300],
              ":hover": {
                bgcolor: red.A400,
              },
            }}
          >
            Clear Conversation
          </Button>
        </Box>
      </Box>
      <Box sx={{ dispay: "flex", flex: { md: 0.8, xs: 1, sm: 1 } }}>
        <Typography
          sx={{
            textAlign: "center",
            fontSize: "40px",
            color: palette.primary.main,
            mb: 2,
          }}
        >
          Model - GPT 4 Turbo
        </Typography>
        <Box
          sx={{
            width: "100%",
            height: "60vh",
            borderRadius: 3,
            mx: "auto",
            display: "flex",
            flexDirection: "column",
            overflow: "scroll",
            overflowX: "hidden",
            overflowY: "auto",
            scrollBehavior: "smooth",
          }}
        >
          {chatMessages.map((chat, index) => (
            <ChatItem content={chat.content} role={chat.role} key={index} />
          ))}
        </Box>
        <div
          style={{
            width: "100%",
            padding: "20px",
            borderRadius: 8,
            backgroundColor: "rgb(17,27,39)",
            display: "flex",
            margin: "auto",
          }}
        >
          {" "}
          <input
            type="text"
            ref={inputRef}
            style={{
              width: "100%",
              backgroundColor: "transparent",
              padding: "10px",
              border: "none",
              outline: "none",
              color: palette.primary.main,
              fontSize: "20px",
            }}
          ></input>
          <IconButton
            onClick={handleSubmit}
            sx={{ m1: "auto", color: palette.primary.main }}
          >
            <IoMdSend />
          </IconButton>
        </div>
      </Box>
    </Box>
  );
};

export default Chat;
