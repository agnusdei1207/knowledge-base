(function () {
  const root = document.documentElement
  const savedTheme = localStorage.getItem("saved-theme") || "light"
  root.setAttribute("saved-theme", savedTheme)

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
  document.querySelector("[data-mobile-explorer]")?.addEventListener("click", () => {
    explorer?.classList.toggle("open")
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

  fetch(window.__SITE_BASE__ || "/knowledge-base/assets/data/site-index.json")
    .catch(() => fetch("/knowledge-base/assets/data/site-index.json"))
    .then((response) => response.ok ? response.json() : Promise.reject(response))
    .then((tree) => {
      const target = document.querySelector("#explorer-tree")
      if (!target) return
      tree.children.forEach((child) => target.appendChild(makeNode(child)))
      document.querySelector(".mobile-explorer")?.classList.remove("hide-until-loaded")
    })
    .catch(() => {
      document.querySelector(".mobile-explorer")?.classList.remove("hide-until-loaded")
    })

  const currentPath = document.querySelector("#backlinks-list")?.dataset.currentPath
  const backlinkKey = currentPath ? encodeURIComponent(currentPath) : ""
  fetch(`/knowledge-base/assets/data/backlinks/${backlinkKey}.json`)
    .then((response) => response.ok ? response.json() : Promise.reject(response))
    .then((links) => {
      const list = document.querySelector("#backlinks-list")
      if (!list || !currentPath) return
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
    .catch(() => {})

  fetch("/knowledge-base/assets/data/graph.json")
    .then((response) => response.ok ? response.json() : Promise.reject(response))
    .then(drawGraph)
    .catch(() => {})

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
  }

  if (window.mermaid) {
    window.mermaid.initialize({ startOnLoad: true, theme: root.getAttribute("saved-theme") === "dark" ? "dark" : "default" })
  }
})()
