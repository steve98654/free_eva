const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const id of ['front','back']){
  const p=await b.newPage({viewport:{width:1200,height:1200},deviceScaleFactor:1});
  await p.goto('file://'+__dirname+'/print.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
  const w=await p.$eval('#'+id,e=>e.getBoundingClientRect().width);
  const fams=await p.evaluate(()=>[...document.fonts].filter(f=>f.status=='loaded').map(f=>f.family+' '+f.weight));
  // target 11 inches wide at 300 dpi = 3300 px
  const dsf=3300/w; await p.close();
  const q=await b.newPage({viewport:{width:1200,height:1200},deviceScaleFactor:dsf});
  await q.goto('file://'+__dirname+'/print.html');await q.evaluate(()=>document.fonts.ready);await q.waitForTimeout(800);
  await q.locator('#'+id).screenshot({path:__dirname+'/bonfire-'+id+'.png',omitBackground:true});
  console.log(id,w,dsf.toFixed(2),[...new Set(fams)].join(', '));
}
await b.close()})()
