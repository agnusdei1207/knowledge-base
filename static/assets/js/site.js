(function () {
  const root = document.documentElement
  const savedTheme = localStorage.getItem("saved-theme") || "light"
  root.setAttribute("saved-theme", savedTheme)
  const basePath = (() => {
    const raw = document.body?.dataset.basepath || ""
    let path = ""
    try {
      path = new URL(raw).pathname.replace(/\/$/, "")
    } catch {
      path = raw.replace(/\/$/, "")
    }
    if (path && window.location.pathname.startsWith(path)) {
      return path
    }
    return ""
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
    if (event.key === "Escape") setMobileExplorerOpen(false)
  })

  const explorer = document.querySelector(".explorer")
  const mobileExplorerButton = document.querySelector("[data-mobile-explorer]")
  const desktopExplorerButton = document.querySelector(".desktop-explorer")
  const explorerContent = document.querySelector(".explorer-content")
  let explorerLoaded = false

  function setMobileExplorerOpen(open) {
    if (!explorer) return
    explorer.classList.toggle("open", open)
    document.body.classList.toggle("explorer-open", open)
    mobileExplorerButton?.setAttribute("aria-expanded", String(open))
  }

  mobileExplorerButton?.addEventListener("click", () => {
    setMobileExplorerOpen(!explorer?.classList.contains("open"))
    loadExplorer()
  })
  explorer?.addEventListener("click", (event) => {
    if (event.target === explorer) {
      setMobileExplorerOpen(false)
    }
  })
  explorerContent?.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement && mobileQuery.matches) {
      setMobileExplorerOpen(false)
    }
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
  const normalizedPath = currentPath && basePath && currentPath.startsWith(basePath)
    ? currentPath.slice(basePath.length)
    : currentPath
  const backlinkKey = normalizedPath ? normalizedPath.replace(/\//g, "_") : ""
  const runWhenIdle = (fn) => {
    if ("requestIdleCallback" in window) {
      window.requestIdleCallback(fn, { timeout: 1500 })
    } else {
      setTimeout(fn, 250)
    }
  }

  if (currentPath) {
    const backlinksPromise = fetch(assetUrl(`/assets/data/backlinks/${backlinkKey}.json`))
      .then((r) => r.ok ? r.json() : [])
      .catch(() => [])

    const graphPromise = fetch(assetUrl(`/assets/data/graphs/${backlinkKey}.json`))
      .then((r) => r.ok ? r.json() : Promise.reject(r))
      .catch(() => fetch(assetUrl("/assets/data/graph.json")).then((r) => r.ok ? r.json() : null).catch(() => null))

    runWhenIdle(() => {
      Promise.all([backlinksPromise, graphPromise]).then(([backlinks, graphData]) => {
        // 1. Render backlinks list
        const list = document.querySelector("#backlinks-list")
        if (list) {
          list.innerHTML = ""
          if (!backlinks.length) {
            const li = document.createElement("li")
            li.className = "meta"
            li.textContent = "No backlinks"
            list.appendChild(li)
          } else {
            backlinks.slice(0, 30).forEach((link) => {
              const li = document.createElement("li")
              const a = document.createElement("a")
              a.className = "internal"
              a.href = link.url
              a.textContent = link.title
              li.appendChild(a)
              list.appendChild(li)
            })
          }
        }

        // 2. Draw graph
        if (graphData && graphData.nodes?.length) {
          drawGraph(graphData)
        }
      })
    })
  }

  function drawGraph(data) {
    const container = document.querySelector("#graph-container")
    if (!container || !data.nodes?.length || typeof cytoscape === "undefined") return

    container.innerHTML = ""

    const currentNorm = decodeURIComponent(window.location.pathname).replace(/\/$/, "")
    const allNodes = data.nodes.map(n => {
      let isCurrent = false
      try {
        const linkNorm = decodeURIComponent(new URL(n.url, window.location.origin).pathname).replace(/\/$/, "")
        isCurrent = (currentNorm === linkNorm && linkNorm !== "")
      } catch {}
      return {
        ...n,
        degree: Number(n.degree || 1),
        group: n.group || "root",
        isCurrent,
      }
    })
    const allNodeById = new Map(allNodes.map(n => [n.id, n]))
    const allLinks = (data.links || [])
      .map((link, index) => ({
        id: `e${index}`,
        source: typeof link.source === "object" ? link.source.id : link.source,
        target: typeof link.target === "object" ? link.target.id : link.target,
      }))
      .filter(link => allNodeById.has(link.source) && allNodeById.has(link.target))

    const currentNode = allNodes.find(n => n.isCurrent)
    const neighborIds = new Set(currentNode ? [currentNode.id] : [])
    if (currentNode) {
      allLinks.forEach(link => {
        if (link.source === currentNode.id) neighborIds.add(link.target)
        if (link.target === currentNode.id) neighborIds.add(link.source)
      })
    }

    const rankedNodes = [...allNodes].sort((a, b) => {
      if (a.isCurrent !== b.isCurrent) return a.isCurrent ? -1 : 1
      if (neighborIds.has(a.id) !== neighborIds.has(b.id)) return neighborIds.has(a.id) ? -1 : 1
      if (a.section !== b.section) return a.section ? -1 : 1
      return b.degree - a.degree
    })
    const selectedIds = new Set(rankedNodes.slice(0, 180).map(n => n.id))
    const graphNodes = rankedNodes.filter(n => selectedIds.has(n.id))
    const graphLinks = allLinks.filter(link => selectedIds.has(link.source) && selectedIds.has(link.target))

    const cs = getComputedStyle(root)
    const colNode = cs.getPropertyValue("--tertiary").trim() || "#6f5f52"
    const colActive = cs.getPropertyValue("--secondary").trim() || "#c96442"
    const colLink = cs.getPropertyValue("--lightgray").trim() || "#e9ded2"
    const colLabel = cs.getPropertyValue("--darkgray").trim() || "#4e463f"
    const colMuted = cs.getPropertyValue("--gray").trim() || "#8a7c70"
    const maxDegree = graphNodes.reduce((max, node) => Math.max(max, node.degree), 1)

    const elements = [
      ...graphNodes.map(node => ({
        classes: [
          node.section ? "section" : "",
          node.isCurrent ? "current" : "",
          neighborIds.has(node.id) ? "neighbor" : "",
        ].filter(Boolean).join(" "),
        data: {
          id: node.id,
          label: node.title || "Untitled",
          url: node.url,
          degree: node.degree,
        },
      })),
      ...graphLinks.map(link => ({
        data: {
          id: link.id,
          source: link.source,
          target: link.target,
        },
      })),
    ]

    const cy = cytoscape({
      container,
      elements,
      wheelSensitivity: 0.14,
      minZoom: 0.25,
      maxZoom: 3,
      style: [
        {
          selector: "node",
          style: {
            "background-color": colNode,
            "border-color": colMuted,
            "border-opacity": 0.38,
            "border-width": 1,
            "color": colLabel,
            "font-family": "var(--bodyFont), sans-serif",
            "font-size": 7,
            "font-weight": 500,
            "height": ele => 6 + Math.sqrt(Number(ele.data("degree")) || 1) / Math.sqrt(maxDegree) * 16,
            "label": ele => {
              if (ele.hasClass("current") || ele.hasClass("section")) return ele.data("label")
              return ""
            },
            "min-zoomed-font-size": 7,
            "overlay-opacity": 0,
            "shape": "ellipse",
            "text-background-color": cs.getPropertyValue("--light").trim() || "#faf7f2",
            "text-background-opacity": 0.82,
            "text-background-padding": 2,
            "text-halign": "center",
            "text-margin-y": -8,
            "text-valign": "top",
            "width": ele => 6 + Math.sqrt(Number(ele.data("degree")) || 1) / Math.sqrt(maxDegree) * 16,
          },
        },
        {
          selector: "node.section",
          style: {
            "background-color": colMuted,
            "height": 14,
            "width": 14,
          },
        },
        {
          selector: "node.current",
          style: {
            "background-color": colActive,
            "border-color": colActive,
            "border-width": 3,
            "height": 22,
            "width": 22,
            "z-index": 20,
          },
        },
        {
          selector: "edge",
          style: {
            "curve-style": "haystack",
            "haystack-radius": 0,
            "line-color": colLink,
            "opacity": 0.36,
            "width": 1,
          },
        },
        {
          selector: ".dimmed",
          style: {
            "opacity": 0.14,
          },
        },
        {
          selector: ".focused",
          style: {
            "label": "data(label)",
            "opacity": 1,
            "z-index": 30,
          },
        },
        {
          selector: "edge.focused",
          style: {
            "line-color": colActive,
            "opacity": 0.92,
            "width": 1.8,
          },
        },
      ],
      layout: {
        name: "cose",
        animate: false,
        componentSpacing: 26,
        idealEdgeLength: 52,
        nodeOverlap: 12,
        nodeRepulsion: 8500,
        padding: 18,
        randomize: false,
      },
    })

    cy.ready(() => {
      cy.fit(undefined, 18)
    })

    function clearFocus() {
      cy.elements().removeClass("dimmed focused")
    }

    cy.on("mouseover", "node", event => {
      const node = event.target
      const neighborhood = node.closedNeighborhood()
      cy.elements().not(neighborhood).addClass("dimmed")
      neighborhood.addClass("focused")
    })

    cy.on("mouseout", "node", clearFocus)

    cy.on("tap", "node", event => {
      const url = event.target.data("url")
      if (url) window.location.href = url
    })

    cy.on("tap", event => {
      if (event.target === cy) clearFocus()
    })
  }

  if (window.mermaid) {
    window.mermaid.initialize({ startOnLoad: true, theme: root.getAttribute("saved-theme") === "dark" ? "dark" : "default" })
  }
})()
