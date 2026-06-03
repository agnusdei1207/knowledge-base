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
    if (!container || !data.nodes?.length || typeof d3 === "undefined") return

    container.innerHTML = ""

    const rect = container.getBoundingClientRect()
    const width = rect.width || 280
    const height = rect.height || 320

    // Resolve current page path
    const currentNorm = decodeURIComponent(window.location.pathname).replace(/\/$/, "")

    // Prepare node data (already filtered and sorted by Python)
    const graphNodes = data.nodes.map(n => {
      let isCurrent = false
      try {
        const linkNorm = decodeURIComponent(new URL(n.url, window.location.origin).pathname).replace(/\/$/, "")
        isCurrent = (currentNorm === linkNorm && linkNorm !== "")
      } catch {}
      return { ...n, degree: Number(n.degree || 1), group: n.group || "root", isCurrent }
    })

    const nodeById = new Map(graphNodes.map(n => [n.id, n]))
    const graphLinks = data.links
      .filter(l => nodeById.has(l.source) && nodeById.has(l.target))
      .map(l => ({ source: l.source, target: l.target }))

    // Build adjacency set for highlight logic
    const adjacency = new Set()
    graphLinks.forEach(l => {
      const sId = typeof l.source === "object" ? l.source.id : l.source
      const tId = typeof l.target === "object" ? l.target.id : l.target
      adjacency.add(`${sId}-${tId}`)
      adjacency.add(`${tId}-${sId}`)
    })
    function isConnected(a, b) {
      return a === b || adjacency.has(`${a}-${b}`)
    }

    // Read theme colors
    const cs = getComputedStyle(root)
    const colNode = cs.getPropertyValue("--tertiary").trim() || "#73826F"
    const colActive = cs.getPropertyValue("--secondary").trim() || "#A65B32"
    const colLink = cs.getPropertyValue("--lightgray").trim() || "#E5DEC9"
    const colLabel = cs.getPropertyValue("--darkgray").trim() || "#383228"
    const colMuted = cs.getPropertyValue("--gray").trim() || "#8E8575"

    const degreeExtent = d3.extent(graphNodes, d => d.degree)
    const radius = d3.scaleSqrt()
      .domain([Math.max(1, degreeExtent[0] || 1), Math.max(2, degreeExtent[1] || 2)])
      .range([3.2, 13])
    const groups = Array.from(new Set(graphNodes.map(d => d.group))).sort()
    const groupIndex = new Map(groups.map((group, index) => [group, index]))
    const clusterRadius = Math.min(width, height) * 0.34
    const clusterCenter = (group) => {
      const index = groupIndex.get(group) || 0
      const angle = groups.length <= 1 ? 0 : (index / groups.length) * Math.PI * 2
      return {
        x: width / 2 + Math.cos(angle) * clusterRadius,
        y: height / 2 + Math.sin(angle) * clusterRadius * 0.72,
      }
    }

    // SVG setup
    const svg = d3.select(container)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", `0 0 ${width} ${height}`)

    // Zoom / pan behaviour
    const g = svg.append("g")
    const zoom = d3.zoom()
      .scaleExtent([0.3, 4])
      .on("zoom", (event) => g.attr("transform", event.transform))
    svg.call(zoom)

    // Force simulation
    const simulation = d3.forceSimulation(graphNodes)
      .force("link", d3.forceLink(graphLinks).id(d => d.id).distance(d => 34 + Math.max(radius(d.source), radius(d.target)) * 3).strength(0.35))
      .force("charge", d3.forceManyBody().strength(d => -70 - radius(d) * 18).distanceMax(260))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("x", d3.forceX(d => clusterCenter(d.group).x).strength(0.08))
      .force("y", d3.forceY(d => clusterCenter(d.group).y).strength(0.08))
      .force("collide", d3.forceCollide(d => radius(d) + 2))
      .alphaDecay(0.025)

    // Draw links
    const linkGroup = g.append("g")
    const linkEls = linkGroup.selectAll("line")
      .data(graphLinks)
      .join("line")
      .attr("stroke", colLink)
      .attr("stroke-width", 0.75)
      .attr("stroke-opacity", 0.34)

    // Draw nodes
    const nodeGroup = g.append("g")
    const nodeEls = nodeGroup.selectAll("circle")
      .data(graphNodes)
      .join("circle")
      .attr("r", d => d.isCurrent ? Math.max(12, radius(d) + 3) : (d.section ? Math.max(7, radius(d)) : radius(d)))
      .attr("fill", d => d.isCurrent ? colActive : colNode)
      .attr("stroke", d => d.isCurrent ? colActive : colMuted)
      .attr("stroke-width", d => d.isCurrent ? 2.2 : 0.7)
      .attr("stroke-opacity", 0.55)
      .attr("fill-opacity", 0.9)
      .attr("cursor", "pointer")
      .call(d3.drag()
        .on("start", dragStart)
        .on("drag", dragged)
        .on("end", dragEnd)
      )

    // Node labels (hidden by default except current, shown on hover/highlight)
    const labelGroup = g.append("g")
    const labelEls = labelGroup.selectAll("text")
      .data(graphNodes)
      .join("text")
      .text(d => {
        const t = d.title || ""
        return t.length > 25 ? t.slice(0, 23) + "…" : t
      })
      .attr("font-size", d => d.isCurrent ? "10px" : "8px")
      .attr("font-weight", d => d.isCurrent || d.degree >= (degreeExtent[1] || 0) * 0.55 ? "700" : "500")
      .attr("font-family", "var(--bodyFont), sans-serif")
      .attr("fill", colLabel)
      .attr("text-anchor", "middle")
      .attr("dy", d => -(radius(d) + 5))
      .attr("pointer-events", "none")
      .attr("opacity", d => d.isCurrent || d.section || d.degree >= (degreeExtent[1] || 0) * 0.42 ? 1 : 0)

    // Tooltip
    const tooltip = d3.select("body").append("div")
      .attr("class", "graph-tooltip")
      .style("display", "none")

    // Hover interactions
    nodeEls
      .on("mouseover", function (event, d) {
        tooltip.style("display", "block").text(d.title)

        // Dim everything, highlight connected
        nodeEls
          .attr("opacity", n => isConnected(d.id, n.id) ? 1 : 0.15)
        linkEls
          .attr("stroke-opacity", l => (l.source.id === d.id || l.target.id === d.id) ? 0.85 : 0.04)
          .attr("stroke-width", l => (l.source.id === d.id || l.target.id === d.id) ? 1.6 : 0.5)
        labelEls
          .attr("opacity", n => isConnected(d.id, n.id) ? 1 : 0)
      })
      .on("mousemove", function (event) {
        tooltip
          .style("left", (event.clientX + 14) + "px")
          .style("top", (event.clientY + 14) + "px")
      })
      .on("mouseout", function () {
        tooltip.style("display", "none")
        nodeEls.attr("opacity", 1)
        linkEls.attr("stroke-opacity", 0.34).attr("stroke-width", 0.75)
        labelEls.attr("opacity", d => d.isCurrent || d.section || d.degree >= (degreeExtent[1] || 0) * 0.42 ? 1 : 0)
      })
      .on("click", function (event, d) {
        if (d.url) window.location.href = d.url
      })

    // Tick — update positions
    simulation.on("tick", () => {
      linkEls
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y)
      nodeEls
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
      labelEls
        .attr("x", d => d.x)
        .attr("y", d => d.y)
    })

    // Drag handlers
    function dragStart(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart()
      d.fx = d.x
      d.fy = d.y
    }
    function dragged(event, d) {
      d.fx = event.x
      d.fy = event.y
    }
    function dragEnd(event, d) {
      if (!event.active) simulation.alphaTarget(0)
      d.fx = null
      d.fy = null
    }
  }

  if (window.mermaid) {
    window.mermaid.initialize({ startOnLoad: true, theme: root.getAttribute("saved-theme") === "dark" ? "dark" : "default" })
  }
})()
