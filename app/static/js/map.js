
(function () {
 const grid = document.getElementById("deptGrid");
 if (!grid) return;

 const deps = [];
 for (let i = 1; i <= 95; i++) deps.push(String(i).padStart(2, "0"));
 deps.push("971", "972", "973", "974", "976");

 deps.forEach((d) => {
   const a = document.createElement("a");
   a.className = "rr-dept-btn";
   a.href = `/map/dept/${encodeURIComponent(d)}`;
   a.textContent = d;
   grid.appendChild(a);
 });
})();