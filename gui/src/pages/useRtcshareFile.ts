import YAML from "js-yaml";
import { useEffect, useState } from "react";
import { useRtcshare } from "../useRtcshare";

export const useRtcshareTextFile = (path: string) => {
    const {client} = useRtcshare()
    const [content, setContent] = useState<string>()
    useEffect(() => {
        if (!client) return
        ;(async () => {
            const a = await client.readFile(path)
            const dec = new TextDecoder()
            setContent(dec.decode(a))
        })()
    }, [client, path])
    return {content}
}

export const useRtcshareYamlFile = (path: string) => {
    const {content} = useRtcshareTextFile(path)
    return {
        content: content ? YAML.load(content) as any : undefined
    }
}

export const useRtcshareJsonFile = (path: string) => {
    const {content} = useRtcshareTextFile(path)
    return {
        content: content ? JSON.parse(content) as any : undefined
    }
}