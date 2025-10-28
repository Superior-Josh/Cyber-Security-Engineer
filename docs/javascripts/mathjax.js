window.MathJax = {
  tex: {
    inlineMath: [["$", "$"], ["\\(", "\\)"]],  // 支持行内公式分隔符
    displayMath: [["$$", "$$"], ["\\[", "\\]"]],  // 支持块级公式分隔符
    processEscapes: true,  // 允许反斜杠转义
    packages: {"[+]": ["ams"]}  // 加载AMS宏包以支持更多符号
  },
  svg: {
    fontCache: "global"
  },
  startup: {
    typeset: false  // 禁用自动排版，改为手动触发
  }
};

// 监听页面动态更新，确保公式重新渲染
document$.subscribe(() => {
  MathJax.startup.output.clearCache();
  MathJax.typesetClear();
  MathJax.texReset();
  MathJax.typesetPromise();
});