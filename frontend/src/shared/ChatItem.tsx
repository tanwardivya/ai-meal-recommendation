import { Box, Avatar, Typography, useTheme } from "@mui/material";
import { RootState } from "@/redux";
import { useSelector } from "react-redux";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { coldarkDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import image1 from "@/assets/openai.png";
import ReactMarkdown from "react-markdown";
import { styled } from "@mui/material/styles";
import remarkGfm from "remark-gfm";
import "../index.css";

// Styled components for various Markdown elements
const StyledParagraph = styled(Typography)({
  fontSize: "1.2rem", // Regular text
});

const StyledHeader1 = styled(Typography)({
  fontSize: "2.5rem", // For h1
  color: "darkblue", // Example color
  fontWeight: "bold",
});

const StyledHeader2 = styled(Typography)({
  fontSize: "2rem", // For h2
  color: "darkgreen",
});

const StyledHeader3 = styled(Typography)({
  fontSize: "1.3rem", // For h3
  color: "darkgreen",
});

const StyledLink = styled(Typography)({
  color: "blue", // Links
  textDecoration: "underline",
});

const StyledList = styled(Typography)({
  paddingLeft: "20px", // Padding for lists
  fontSize: "1.2rem",
});

const markdownComponents = {
  p: ({ ...props }) => <StyledParagraph {...props} />,
  h1: ({ ...props }) => <StyledHeader1 variant="h1" {...props} />,
  h2: ({ ...props }) => <StyledHeader2 variant="h2" {...props} />,
  h3: ({ ...props }) => <StyledHeader3 variant="h3" {...props} />,
  a: ({ ...props }) => <StyledLink {...props} />,
  ul: ({ ...props }) => <StyledList {...props} />,
  ol: ({ ...props }) => <StyledList {...props} />,
};

function extractCodeFromString(message: string) {
  if (message.includes("```")) {
    const blocks = message.split("```");
    return blocks;
  }
}

function isCodeBlock(str: string) {
  if (
    str.includes("=") ||
    str.includes(";") ||
    str.includes("[") ||
    str.includes("]") ||
    str.includes("{") ||
    str.includes("}") ||
    str.includes("#") ||
    str.includes("//")
  ) {
    return true;
  }
  return false;
}
const ChatItem = ({
  content,
  role,
}: {
  content: string;
  role: "user" | "assistant";
}) => {
  const messageBlocks = extractCodeFromString(content);
  const user = useSelector((state: RootState) => state.user);
  const { palette } = useTheme();
  return role == "assistant" ? (
    <Box
      sx={{
        display: "flex",
        p: 2,
        bgcolor: "#004d5612",
        gap: 2,
        borderRadius: 2,
        my: 1,
      }}
    >
      <Avatar sx={{ ml: "0" }}>
        <img src={image1} alt="openai" width={"30px"} />
      </Avatar>
      <Box>
        {!messageBlocks && (
          <ReactMarkdown
            components={markdownComponents}
            remarkPlugins={[remarkGfm]}
            className="markdown-content"
          >
            {content}
          </ReactMarkdown>
        )}
        {messageBlocks &&
          messageBlocks.length &&
          messageBlocks.map((block) =>
            isCodeBlock(block) ? (
              <SyntaxHighlighter style={coldarkDark} language="javascript">
                {block}
              </SyntaxHighlighter>
            ) : (
              <Typography sx={{ fontSize: "20px" }}>{block}</Typography>
            ),
          )}
      </Box>
    </Box>
  ) : (
    <Box
      sx={{
        display: "flex",
        p: 2,
        bgcolor: "#004d56",
        gap: 2,
        borderRadius: 2,
      }}
    >
      <Avatar sx={{ ml: "0", bgcolor: "black", color: palette.primary.main }}>
        {user?.firstname[0]}
        {user?.lastname[0]}
      </Avatar>
      <Box>
        {!messageBlocks && (
          <Typography sx={{ fontSize: "20px", color: "white" }}>
            {content}
          </Typography>
        )}
        {messageBlocks &&
          messageBlocks.length &&
          messageBlocks.map((block) =>
            isCodeBlock(block) ? (
              <SyntaxHighlighter style={coldarkDark} language="javascript">
                {block}
              </SyntaxHighlighter>
            ) : (
              <Typography sx={{ fontSize: "20px" }}>{block}</Typography>
            ),
          )}
      </Box>
    </Box>
  );
};

export default ChatItem;
