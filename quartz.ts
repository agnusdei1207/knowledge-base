import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import { componentRegistry } from "./quartz/components/registry"

type ExplorerNode = {
  displayName?: string
}

componentRegistry.setOptionOverrides("explorer", {
  title: "Explorer",
  mapFn: (node: ExplorerNode) => {
    const emojiPattern =
      /[\p{Emoji_Presentation}\p{Extended_Pictographic}\uFE0F\u200D\u20E3]|\p{Regional_Indicator}/gu
    const stripEmoji = (value: string) =>
      value
        .replace(emojiPattern, "")
        .replace(/\s{2,}/g, " ")
        .trim()

    if (typeof node.displayName === "string") {
      node.displayName = stripEmoji(node.displayName)
    }

    return node
  },
})

const config = await loadQuartzConfig()
export default config
export const layout = await loadQuartzLayout()
