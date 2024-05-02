import { Box, BoxProps } from "@mui/material";
import { styled, SxProps } from "@mui/system";

interface FlexBetweenProps extends BoxProps {
  sx?: SxProps; // This allows you to use the sx prop for additional styles
}

const FlexBetween = styled(Box)<FlexBetweenProps>(({ theme, sx }) => ({
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    ...sx, // Spread the sx prop for custom styles
  }));

export default FlexBetween;