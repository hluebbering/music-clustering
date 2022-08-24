hljs.registerLanguage("bash",
  function(e){
    var r="([a-zA-Z]|\\.[a-zA-Z.])[a-zA-Z0-9._]*";
    return{
      c:[e.HCM,
      {b:r,l:r,k:
        {keyword:"Load",
        literal:"NULL NA TRUE FALSE T F",
          bashkey: "data not"
        }, 
        r:0},
      {cN:"number",b:"0[xX][0-9a-fA-F]+[Li]?\\b",r:0},
      {cN:"number",b:"\\d+(?:[eE][+\\-]?\\d*)?L\\b",r:0},
      {cN:"number",b:"\\d+\\.(?!\\d)(?:i\\b)?",r:0},
      {cN:"number",b:"\\d+(?:\\.\\d*)?(?:[eE][+\\-]?\\d*)?i?\\b",r:0},
      {cN:"number",b:"\\.\\d+(?:[eE][+\\-]?\\d*)?i?\\b",r:0},
      {cN:"pipe",b:"%>%",r:0},
      {b:"`",e:"`",r:0},
      {cN:"string",c:[e.BE],v:[{b:'"',e:'"'},{b:"'",e:"'"}]},
      {cN: "keyword", b: /(^|\s*)(:::?|\.)\w+(?=\(|$)/}, ]}});

hljs.initHighlightingOnLoad();