import axios from "axios";

export const sendChatRequest = async (message: string, token: string) => {
    const res = await axios.post("/chat/new", {message},
        {headers:{
            "Authorization": "Bearer ".concat(token)
        }
    }
    );
    if (res.status !== 200){
        throw new Error("Unable to send chat");
    }
    const data = await res.data;
    return data
}

export const deleteChatRequest = async (token: string) => {
    const res = await axios.delete("/chat/delete",
        {headers:{
            "Authorization": "Bearer ".concat(token)
        }
        }
    )
    if (res.status == 204){
        return
    }
    throw new Error("Unable to delete chat");
}