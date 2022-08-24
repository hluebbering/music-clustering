hljs.registerLanguage("python",function(e){
  var t={
    keyword: "and elif is global as in if from raise except finally import pass exec else break not with class assert yield try while continue del or lambda async await nonlocal|10 None",
    pybuilt: "for in return",
    pykey: "parse print len",
    logc: "True False",
    pyfunc:  "range list dict float",
    pypd: "read_csv def",
    myfunc: "euclidean_distance common_artists"
  },
  r={cN:"meta",b:/^(>>>|\.\.\.) /},
  a={cN:"subst",b:/\{/,e:/\}/,k:t,i:/#/},
  n={
    cN:"string",
    c:[e.BE],
    v:[
      {b:/(u|b)?r?'''/,e:/'''/,c:[e.BE,r],r:10},
      {b:/(u|b)?r?"""/,e:/"""/,c:[e.BE,r],r:10},
      {b:/(fr|rf|f)'''/,e:/'''/,c:[e.BE,r,a]},
      {b:/(fr|rf|f)"""/,e:/"""/,c:[e.BE,r,a]},
      {b:/(u|r|ur)'/,e:/'/,r:10},
      {b:/(u|r|ur)"/,e:/"/,r:10},
      {b:/(b|br)'/,e:/'/},
      {b:/(b|br)"/,e:/"/},
      {b:/(fr|rf|f)'/,e:/'/,c:[e.BE,a]},
      {b:/(fr|rf|f)"/,e:/"/,c:[e.BE,a]},e.ASM,e.QSM
    ]
  },
  i={cN:"number",r:0,v:[{b:e.BNR+"[lLjJ]?"},{b:"\\b(0o[0-7]+)[lLjJ]?"},{b:e.CNR+"[lLjJ]?"}]},
  s={cN:"params",b:/\(/,e:/\)/,c:["self",r,i,n]};
  
  return a.c=[n,i,r],
  {
    aliases:["py","gyp"],
    k:t,i:/(<\/|->|\?)|=>/,
    c:[r,i,n,e.HCM,
    {
      v:[{cN:"function",bK:"def"},
      {cN:"class",bK:"class"}],
      e:/:/,i:/[${=;\n,]/,
      c:[e.UTM,s,{b:/->/,eW:!0,k:"None"}]
    },
    {cN:"meta",b:/^[\t ]*@/,e:/$/},
    {b:/\b(printt|exec)\(/}]
  };
});

hljs.initHighlightingOnLoad();