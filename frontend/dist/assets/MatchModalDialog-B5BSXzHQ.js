import{d as ge,I as _e,J as C,r as h,h as w,w as n,N as we,f,b as o,K as j,x as c,t as m,n as R,e as i,c as X,v as T,k as b,p as Z,q as ee,s as A,u as te,M as ae,B as De,z as x,G as E,D as L,L as Ve,O as se,A as I,C as ye,_ as ke}from"./index-DD0chK9m.js";import{V as O}from"./VDialog-8pvQ3nO6.js";import{V as J}from"./VAlert-BswZB0pH.js";import{V as oe}from"./VSpacer-DKUpOtpE.js";import{V as Ce}from"./VForm-D4HHFwdz.js";import{V as le}from"./VAutocomplete-CIS9KaFs.js";const Te={class:"match-details-centered"},be={class:"tournament-stage"},Me={class:"is-finished"},$e={class:"match-layout"},Se={class:"team-info-left"},Ue={class:"avatar-container"},Ee={class:"team-info-right"},Fe={class:"avatar-container"},Ae={class:"match-time"},Ie={class:"time-text"},He={key:0,class:"winner"},ze={class:"winner-name"},Be={class:"dialog-content"},Ne={class:"dialog-content"},Pe={class:"team-slot"},je={class:"d-flex align-center"},Re={class:"team-slot"},xe={class:"d-flex align-center"},Le=ge({__name:"MatchModalDialog",props:{modelValue:{type:Boolean},match:{},tournamentDirectorId:{},onMatchUpdate:{type:Function}},emits:["update:modelValue","match-updated"],setup(ne,{emit:ie}){const l=ne,re=ie,D=_e(),H=C({get:()=>l.modelValue,set:t=>re("update:modelValue",t)}),M=h(!1),$=h(!1),u=h(""),g=h(""),_=h(""),V=h([]),F=h(!1),me=h(null),v=h(""),y=h(""),z=h(!1),B=h(!1),de=[t=>new Date(t)>new Date||"Match time cannot be in the past",t=>{const e=new Date(t),s=new Date;return s.setDate(s.getDate()+1),s.setHours(e.getHours(),e.getMinutes(),e.getSeconds()),e>s||"Match time must be at least 1 day in the future"}],k=C(()=>(console.log("director_id:",l.tournamentDirectorId),console.log("user_id:",D.userId),D.isAuthenticated&&(D.userRole==="admin"||l.tournamentDirectorId===D.userId))),q=C(()=>{if(!l.match||!u.value)return!1;const t=new Date(l.match.start_time),e=new Date(u.value);return t.getTime()!==e.getTime()&&N.value}),N=C(()=>{if(!u.value)return!0;const t=new Date(u.value),e=new Date,s=new Date;return s.setDate(s.getDate()+1),s.setHours(t.getHours(),t.getMinutes(),t.getSeconds()),t>e&&t>s}),ce=C(()=>{if(!u.value)return"";const t=new Date(u.value),e=new Date,s=new Date;return s.setDate(s.getDate()+1),s.setHours(t.getHours(),t.getMinutes(),t.getSeconds()),t<=e?"Match time cannot be in the past":t<=s?"Match time must be at least 1 day in the future":""}),G=C(()=>{if(!l.match)return!1;const t=g.value&&g.value!==l.match.team1_id,e=_.value&&_.value!==l.match.team2_id;return t||e}),ue=()=>{H.value=!1},P=async t=>{var e;try{const s=await t.text(),a=JSON.parse(s);return a.detail&&Array.isArray(a.detail)&&((e=a.detail[0])!=null&&e.msg)?a.detail[0].msg:a.detail?a.detail:"An error occurred"}catch(s){return console.error("Error extracting message:",s),"An error occurred"}},K=async t=>{if(l.match)try{y.value="";const e=await fetch(`${I}/matches/${l.match.id}/team-scores?team_to_upvote_score=${t}`,{method:"PUT",headers:{Authorization:`Bearer ${D.token}`,"Content-Type":"application/json"}});if(!e.ok){y.value=await P(e);return}l.onMatchUpdate&&await l.onMatchUpdate()}catch(e){console.error("Error updating score:",e),y.value="An unexpected error occurred while updating the score"}},ve=async()=>{if(!(!l.match||!u.value||!N.value))try{v.value="",z.value=!0;const t=new Date(u.value);t.setHours(t.getHours()+2);const e=t.toISOString(),s=await fetch(`${I}/matches/${l.match.id}?start_time=${encodeURIComponent(e)}`,{method:"PUT",headers:{Authorization:`Bearer ${D.token}`,"Content-Type":"application/json"}});if(!s.ok){v.value=await P(s);return}const a=await s.json();l.match&&Object.assign(l.match,a),l.onMatchUpdate&&await l.onMatchUpdate(),M.value=!1}catch(t){console.error("Full error:",t),v.value="Failed to update match time"}finally{z.value=!1}},he=()=>{if(!l.match)return;const t=new Date(l.match.start_time),e=t.getFullYear(),s=String(t.getMonth()+1).padStart(2,"0"),a=String(t.getDate()).padStart(2,"0"),r=String(t.getHours()).padStart(2,"0"),p=String(t.getMinutes()).padStart(2,"0");u.value=`${e}-${s}-${a}T${r}:${p}`,M.value=!0},fe=async()=>{try{F.value=!0,v.value="";const t=await fetch(`${I}/teams/?is_available=true&offset=0&limit=100`);if(!t.ok)throw new Error("Failed to load teams");const e=await t.json();if(V.value=e,l.match){const s=e.some(r=>{var p;return r.id===((p=l.match)==null?void 0:p.team1_id)}),a=e.some(r=>{var p;return r.id===((p=l.match)==null?void 0:p.team2_id)});!s&&l.match.team1_id&&V.value.push({id:l.match.team1_id,name:l.match.team1_name}),!a&&l.match.team2_id&&V.value.push({id:l.match.team2_id,name:l.match.team2_name}),g.value=l.match.team1_id,_.value=l.match.team2_id}$.value=!0}catch(t){console.error("Error fetching teams:",t),v.value="Failed to load teams"}finally{F.value=!1}},pe=async()=>{if(l.match)try{v.value="",B.value=!0;let t=new URLSearchParams;if(g.value){const e=V.value.find(s=>s.id===g.value);e&&t.append("team1_name",e.name)}if(_.value){const e=V.value.find(s=>s.id===_.value);e&&t.append("team2_name",e.name)}if(t.toString()){const e=await fetch(`${I}/matches/${l.match.id}?${t.toString()}`,{method:"PUT",headers:{Authorization:`Bearer ${D.token}`}});if(!e.ok){const s=await P(e);throw new Error(s)}l.onMatchUpdate&&await l.onMatchUpdate(),$.value=!1}}catch(t){console.error("Error updating teams:",t),v.value=t.message||"Failed to update teams"}finally{B.value=!1}};return(t,e)=>{const s=we("router-link");return f(),w(O,{modelValue:H.value,"onUpdate:modelValue":e[11]||(e[11]=a=>H.value=a),"max-width":"800px",height:"550",class:"match-dialog"},{default:n(()=>[o(L,{class:"custom-dialog-card"},{default:n(()=>[o(j,{class:"headline text-center"},{default:n(()=>{var a,r;return[c(m((a=t.match)==null?void 0:a.team1_name)+" vs "+m((r=t.match)==null?void 0:r.team2_name),1)]}),_:1}),o(R,null,{default:n(()=>{var a,r,p,Y,Q,W;return[i("div",Te,[o(s,{to:`/events/${(a=t.match)==null?void 0:a.tournament_id}`,class:"tournament-title tournament-link"},{default:n(()=>{var d;return[c(m((d=t.match)==null?void 0:d.tournament_title),1)]}),_:1},8,["to"]),i("div",be,m((r=t.match)==null?void 0:r.stage),1),i("div",Me,m((p=t.match)!=null&&p.is_finished?"Finished":"Not finished"),1),i("div",$e,[i("div",Se,[i("div",Ue,[k.value?(f(),X("div",{key:0,class:"edit-container",onClick:fe},[o(T,{icon:"mdi-pencil",class:"edit-icon"}),e[12]||(e[12]=i("span",{class:"edit-text"},"Edit Teams",-1))])):b("",!0),o(Z,{location:"top"},{activator:n(({props:d})=>{var S;return[o(s,{to:`/teams/${(S=t.match)==null?void 0:S.team1_id}`,class:"team-avatar-link"},{default:n(()=>[o(ee,A({class:"team-avatar",size:"150"},d),{default:n(()=>{var U;return[(U=t.match)!=null&&U.team1_logo?(f(),w(te,{key:0,src:t.match.team1_logo,alt:t.match.team1_name},null,8,["src","alt"])):(f(),w(T,{key:1,icon:"mdi-account",color:"#42DDF2FF",size:"40"}))]}),_:2},1040)]),_:2},1032,["to"])]}),default:n(()=>{var d;return[c(" "+m((d=t.match)==null?void 0:d.team1_name),1)]}),_:1})]),i("span",{class:ae(["team-score",{clickable:k.value}]),onClick:e[0]||(e[0]=d=>k.value&&K("team1"))},m((Y=t.match)==null?void 0:Y.team1_score),3)]),e[13]||(e[13]=i("div",{class:"score-divider"},":",-1)),i("div",Ee,[i("span",{class:ae(["team-score",{clickable:k.value}]),onClick:e[1]||(e[1]=d=>k.value&&K("team2"))},m((Q=t.match)==null?void 0:Q.team2_score),3),i("div",Fe,[o(Z,{location:"top"},{activator:n(({props:d})=>{var S;return[o(s,{to:`/teams/${(S=t.match)==null?void 0:S.team2_id}`,class:"team-avatar-link"},{default:n(()=>[o(ee,A({class:"team-avatar",size:"150"},d),{default:n(()=>{var U;return[(U=t.match)!=null&&U.team2_logo?(f(),w(te,{key:0,src:t.match.team2_logo,alt:t.match.team2_name},null,8,["src","alt"])):(f(),w(T,{key:1,icon:"mdi-account",color:"#42DDF2FF",size:"40"}))]}),_:2},1040)]),_:2},1032,["to"])]}),default:n(()=>{var d;return[c(" "+m((d=t.match)==null?void 0:d.team2_name),1)]}),_:1})])])]),i("div",Ae,[o(T,{icon:"mdi-clock-outline",class:"mr-2 neon-text"}),i("span",Ie,m(t.match?De(ye)(new Date(t.match.start_time),"HH:mm, dd MMM yyyy"):""),1),k.value?(f(),w(T,{key:0,icon:"mdi-pencil",class:"edit-icon ml-2",onClick:he})):b("",!0)]),(W=t.match)!=null&&W.winner_id?(f(),X("div",He,[o(T,{icon:"mdi-crown",color:"#fed854",size:"24"}),i("span",ze,m(t.match.winner_id===t.match.team1_id?t.match.team1_name:t.match.team2_name),1)])):b("",!0)])]}),_:1}),o(x,null,{default:n(()=>[y.value?(f(),w(J,{key:0,type:"error",variant:"tonal",class:"mb-4 error-alert",closable:"","onClick:close":e[2]||(e[2]=a=>y.value="")},{default:n(()=>[c(m(y.value),1)]),_:1})):b("",!0),o(E,{onClick:ue},{default:n(()=>e[14]||(e[14]=[c("Close")])),_:1})]),_:1})]),_:1}),o(O,{modelValue:M.value,"onUpdate:modelValue":e[6]||(e[6]=a=>M.value=a),"max-width":"500px",class:"time-edit-dialog"},{default:n(()=>[o(L,{class:"edit-dialog"},{default:n(()=>[i("div",Be,[o(j,{class:"dialog-title"},{default:n(()=>e[15]||(e[15]=[c("Edit Match Time")])),_:1}),o(R,null,{default:n(()=>[v.value?(f(),w(J,{key:0,type:"error",variant:"tonal",class:"mb-4 error-alert",closable:"","onClick:close":e[3]||(e[3]=a=>v.value="")},{default:n(()=>[c(m(v.value),1)]),_:1})):b("",!0),o(Ve,{modelValue:u.value,"onUpdate:modelValue":e[4]||(e[4]=a=>u.value=a),label:"Match Time",type:"datetime-local",variant:"outlined",rules:de,error:!N.value&&!!u.value,"error-messages":ce.value,class:"time-field custom-time-field","persistent-hint":""},null,8,["modelValue","error","error-messages"])]),_:1}),o(x,{class:"dialog-actions"},{default:n(()=>[o(oe),o(E,{class:"cancel-btn",variant:"text",onClick:e[5]||(e[5]=a=>M.value=!1)},{default:n(()=>e[16]||(e[16]=[c(" Cancel ")])),_:1}),o(E,{class:"submit-btn",onClick:ve,loading:z.value,disabled:!q.value},{default:n(()=>[c(m(q.value?"Save":"No Changes"),1)]),_:1},8,["loading","disabled"])]),_:1})])]),_:1})]),_:1},8,["modelValue"]),o(O,{modelValue:$.value,"onUpdate:modelValue":e[10]||(e[10]=a=>$.value=a),"max-width":"500px",class:"team-edit-dialog"},{default:n(()=>[o(L,{class:"dialog-card"},{default:n(()=>[i("div",Ne,[o(j,{class:"dialog-title"},{default:n(()=>e[17]||(e[17]=[c("Edit Teams")])),_:1}),o(R,null,{default:n(()=>[v.value?(f(),w(J,{key:0,type:"error",variant:"tonal",class:"mb-4"},{default:n(()=>[c(m(v.value),1)]),_:1})):b("",!0),o(Ce,{ref_key:"teamForm",ref:me},{default:n(()=>[i("div",Pe,[i("div",je,[o(le,{modelValue:g.value,"onUpdate:modelValue":e[7]||(e[7]=a=>g.value=a),items:V.value,"item-title":"name","item-value":"id",label:"Team 1",variant:"outlined",loading:F.value,"model-value":g.value,clearable:"",class:"custom-autocomplete","menu-props":{contentClass:"teams-menu"}},{item:n(({props:a,item:r})=>[o(se,A(a,{title:r.raw.name,class:["team-list-item",{"team-list-item--selected":r.raw.id===g.value}]}),null,16,["title","class"])]),_:1},8,["modelValue","items","loading","model-value"])])]),i("div",Re,[i("div",xe,[o(le,{modelValue:_.value,"onUpdate:modelValue":e[8]||(e[8]=a=>_.value=a),items:V.value,"item-title":"name","item-value":"id",label:"Team 2",variant:"outlined",loading:F.value,"model-value":_.value,clearable:"",class:"custom-autocomplete","menu-props":{contentClass:"teams-menu"}},{item:n(({props:a,item:r})=>[o(se,A(a,{title:r.raw.name,class:["team-list-item",{"team-list-item--selected":r.raw.id===_.value}]}),null,16,["title","class"])]),_:1},8,["modelValue","items","loading","model-value"])])])]),_:1},512)]),_:1}),o(x,{class:"dialog-actions"},{default:n(()=>[o(oe),o(E,{class:"cancel-btn",variant:"text",onClick:e[9]||(e[9]=a=>$.value=!1)},{default:n(()=>e[18]||(e[18]=[c(" Cancel ")])),_:1}),o(E,{class:"submit-btn",onClick:pe,loading:B.value,disabled:!G.value},{default:n(()=>[c(m(G.value?"Save":"No Changes"),1)]),_:1},8,["loading","disabled"])]),_:1})])]),_:1})]),_:1},8,["modelValue"])]),_:1},8,["modelValue"])}}}),Qe=ke(Le,[["__scopeId","data-v-05e36394"]]);export{Qe as M};