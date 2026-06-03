(function () {
  const root = document.documentElement
  const savedTheme = localStorage.getItem("saved-theme") || "light"
  root.setAttribute("saved-theme", savedTheme)
  const basePath = (() => {
    const raw = document.body?.dataset.basepath || ""
    try {
      return new URL(raw).pathname.replace(/\/$/, "")
    } catch {
      return raw.replace(/\/$/, "")
    }
  })()
  const assetUrl = (path) => `${basePath}${path.startsWith("/") ? path : `/${path}`}`
  const mobileQuery = window.matchMedia("(max-width: 800px)")

  const themeButton = document.querySelector("[data-theme-toggle]")
  themeButton?.addEventListener("click", () => {
    const next = root.getAttribute("saved-theme") === "dark" ? "light" : "dark"
    root.setAttribute("saved-theme", next)
    localStorage.setItem("saved-theme", next)
  })

  const modal = document.querySelector("[data-search-modal]")
  const openSearch = document.querySelector("[data-search-open]")
  const closeSearch = document.querySelector("[data-search-close]")
  let pagefindReady = false

  function openSearchModal() {
    if (!modal) return
    modal.hidden = false
    openSearch?.setAttribute("aria-expanded", "true")
    if (!pagefindReady && window.PagefindUI) {
      new window.PagefindUI({
        element: "#search",
        showSubResults: true,
        showImages: false,
      })
      pagefindReady = true
    }
    setTimeout(() => modal.querySelector("input")?.focus(), 30)
  }

  function closeSearchModal() {
    if (!modal) return
    modal.hidden = true
    openSearch?.setAttribute("aria-expanded", "false")
  }

  openSearch?.addEventListener("click", openSearchModal)
  closeSearch?.addEventListener("click", closeSearchModal)
  modal?.addEventListener("click", (event) => {
    if (event.target === modal) closeSearchModal()
  })
  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault()
      openSearchModal()
    }
    if (event.key === "Escape") closeSearchModal()
  })

  const explorer = document.querySelector(".explorer")
  const mobileExplorerButton = document.querySelector("[data-mobile-explorer]")
  const desktopExplorerButton = document.querySelector(".desktop-explorer")
  const explorerContent = document.querySelector(".explorer-content")
  let explorerLoaded = false

  mobileExplorerButton?.addEventListener("click", () => {
    explorer?.classList.toggle("open")
    loadExplorer()
  })
  desktopExplorerButton?.addEventListener("click", () => {
    explorer?.classList.toggle("collapsed")
    const expanded = !explorer?.classList.contains("collapsed")
    desktopExplorerButton.setAttribute("aria-expanded", String(expanded))
    explorerContent?.setAttribute("aria-expanded", String(expanded))
  })

  const toc = document.querySelector(".toc")
  const tocButton = document.querySelector(".toc-header")
  tocButton?.addEventListener("click", () => {
    toc?.classList.toggle("collapsed")
    tocButton.setAttribute("aria-expanded", String(!toc?.classList.contains("collapsed")))
  })

  function makeNode(item) {
    const li = document.createElement("li")
    li.className = "explorer-item"
    let hasActiveChild = false

    if (item.children && item.children.length) {
      li.classList.add("folder", "collapsed")
      const button = document.createElement("button")
      button.className = "folder-button"
      button.type = "button"
      button.textContent = item.title
      button.addEventListener("click", () => li.classList.toggle("collapsed"))
      li.appendChild(button)
      const ul = document.createElement("ul")
      item.children.forEach((child) => {
        const childNode = makeNode(child)
        if (childNode.dataset.active === "true" || childNode.dataset.hasActiveChild === "true") {
          hasActiveChild = true
        }
        ul.appendChild(childNode)
      })
      li.appendChild(ul)
      
      if (hasActiveChild) {
        li.classList.remove("collapsed")
        li.dataset.hasActiveChild = "true"
      }
    } else {
      const a = document.createElement("a")
      a.className = "explorer-link internal"
      a.href = item.url
      a.textContent = item.title
      li.appendChild(a)
      
      const currentNorm = decodeURIComponent(window.location.pathname).replace(/\/$/, "")
      const linkNorm = decodeURIComponent(a.pathname).replace(/\/$/, "")
      if (currentNorm === linkNorm && linkNorm !== "") {
        a.classList.add("active")
        li.dataset.active = "true"
      }
    }
    return li
  }

  function loadExplorer() {
    if (explorerLoaded) return
    explorerLoaded = true
    fetch(assetUrl("/assets/data/site-index.json"))
      .then((response) => response.ok ? response.json() : Promise.reject(response))
      .then((tree) => {
        const target = document.querySelector("#explorer-tree")
        if (!target) return
        tree.children.forEach((child) => target.appendChild(makeNode(child)))
        mobileExplorerButton?.classList.remove("hide-until-loaded")
      })
      .catch(() => {
        mobileExplorerButton?.classList.remove("hide-until-loaded")
      })
  }

  if (!mobileQuery.matches) {
    loadExplorer()
  } else {
    mobileExplorerButton?.classList.remove("hide-until-loaded")
  }

  const currentPath = document.querySelector("#backlinks-list")?.dataset.currentPath
  const backlinkKey = currentPath ? encodeURIComponent(currentPath) : ""
  const runWhenIdle = (fn) => {
    if ("requestIdleCallback" in window) {
      window.requestIdleCallback(fn, { timeout: 1500 })
    } else {
      setTimeout(fn, 250)
    }
  }

  if (currentPath) {
    runWhenIdle(() => fetch(assetUrl(`/assets/data/backlinks/${backlinkKey}.json`))
      .then((response) => response.ok ? response.json() : Promise.reject(response))
      .then((links) => {
        const list = document.querySelector("#backlinks-list")
        if (!list) return
        if (!links.length) {
          const li = document.createElement("li")
          li.className = "meta"
          li.textContent = "백링크 없음"
          list.appendChild(li)
          return
        }
        links.slice(0, 30).forEach((link) => {
          const li = document.createElement("li")
          const a = document.createElement("a")
          a.className = "internal"
          a.href = link.url
          a.textContent = link.title
          li.appendChild(a)
          list.appendChild(li)
        })
      })
      .catch(() => {}))
  }

  runWhenIdle(() => {
    fetch(assetUrl("/assets/data/graph.json"))
      .then((response) => response.ok ? response.json() : Promise.reject(response))
      .then(drawGraph)
      .catch(() => {})
  })

  function drawGraph(data) {
    const canvas = document.querySelector("#global-graph")
    if (!canvas || !data.nodes?.length) return
    const ctx = canvas.getContext("2d")
    const rect = canvas.getBoundingClientRect()
    const dpr = window.devicePixelRatio || 1
    canvas.width = Math.max(1, rect.width * dpr)
    canvas.height = Math.max(1, rect.height * dpr)
    ctx.scale(dpr, dpr)
    const width = rect.width
    const height = rect.height
    const nodes = data.nodes.slice(0, 120).map((node, index) => {
      const angle = (index / Math.min(data.nodes.length, 120)) * Math.PI * 2
      const radius = 35 + (index % 5) * 18
      return {
        ...node,
        x: width / 2 + Math.cos(angle) * radius,
        y: height / 2 + Math.sin(angle) * radius,
      }
    })
    const byId = new Map(nodes.map((node) => [node.id, node]))
    ctx.clearRect(0, 0, width, height)
    ctx.strokeStyle = getComputedStyle(root).getPropertyValue("--lightgray")
    ctx.fillStyle = getComputedStyle(root).getPropertyValue("--tertiary")
    data.links.slice(0, 220).forEach((link) => {
      const source = byId.get(link.source)
      const target = byId.get(link.target)
      if (!source || !target) return
      ctx.beginPath()
      ctx.moveTo(source.x, source.y)
      ctx.lineTo(target.x, target.y)
      ctx.stroke()
    })
    nodes.forEach((node) => {
      ctx.beginPath()
      ctx.arc(node.x, node.y, node.section ? 3.2 : 2.2, 0, Math.PI * 2)
      ctx.fill()
    })
    const tooltip = document.createElement("div")
    tooltip.className = "graph-tooltip"
    tooltip.hidden = true
    document.body.appendChild(tooltip)

    function nearestNode(event) {
      const box = canvas.getBoundingClientRect()
      const x = event.clientX - box.left
      const y = event.clientY - box.top
      let nearest = null
      let distance = 16
      for (const node of nodes) {
        const current = Math.hypot(node.x - x, node.y - y)
        if (current < distance) {
          nearest = node
          distance = current
        }
      }
      return nearest
    }

    canvas.addEventListener("mousemove", (event) => {
      const node = nearestNode(event)
      if (!node) {
        tooltip.hidden = true
        canvas.style.cursor = "default"
        return
      }
      tooltip.hidden = false
      tooltip.textContent = node.title
      tooltip.style.left = `${event.clientX + 12}px`
      tooltip.style.top = `${event.clientY + 12}px`
      canvas.style.cursor = "pointer"
    })
    canvas.addEventListener("mouseleave", () => {
      tooltip.hidden = true
      canvas.style.cursor = "default"
    })
    canvas.addEventListener("click", (event) => {
      const node = nearestNode(event)
      if (node?.url) window.location.href = node.url
    })
  }

  if (window.mermaid) {
    window.mermaid.initialize({ startOnLoad: true, theme: root.getAttribute("saved-theme") === "dark" ? "dark" : "default" })
  }
})()
