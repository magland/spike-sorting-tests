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

export const useRtcshareTextFiles = (paths: string[]) => {
    const {client} = useRtcshare()
    const [contents, setContents] = useState<(string | undefined)[]>()
    useEffect(() => {
        if (!client) return
        ;(async () => {
            const contents0: (string | undefined)[] = []
            for (const path of paths) {
                try {
                    const a = await client.readFile(path)
                    const dec = new TextDecoder()
                    contents0.push(dec.decode(a))
                }
                catch(err) {
                    contents0.push(undefined)
                }
            }
            setContents(contents0)
        })()
    }, [client, paths])
    return {contents}
}

export const useRtcshareJsonFiles = (paths: string[]) => {
    const {contents} = useRtcshareTextFiles(paths)
    return {
        contents: contents ? contents.map(c => (c ? JSON.parse(c) as any : undefined)) : undefined
    }
}