import{V as p}from"./VSelect-BpGEebQz.js";import{d as V,r as v,m as C,f as h,h as D,w as r,b as o,l as _,j as w,_ as F,c as B,e as a,t as i,v as b,x as M,G as S,C as g}from"./index-DD0chK9m.js";const U=V({__name:"TournamentFilterBar",emits:["filter-change"],setup(x,{emit:c}){const d=c,n=v(null),t=v(null),e=v(null),m=[{text:"Upcoming",value:"future"},{text:"Current",value:"present"},{text:"Past",value:"past"}],f=[{text:"Active",value:"active"},{text:"Finished",value:"finished"}],y=[{text:"Single Elimination",value:"single elimination"},{text:"Round Robin",value:"round robin"},{text:"One Off Match",value:"one off match"}],u=()=>{d("filter-change",{period:n.value,status:t.value,format:e.value})};return C([n,t,e],()=>{u()}),(E,s)=>(h(),D(w,{class:"filter-row"},{default:r(()=>[o(_,{cols:"12",md:"3"},{default:r(()=>[o(p,{modelValue:n.value,"onUpdate:modelValue":[s[0]||(s[0]=l=>n.value=l),u],items:m,"item-title":"text","item-value":"value",label:"Period",variant:"outlined",density:"comfortable","bg-color":"rgba(45, 55, 75, 0.4)",color:"#42DDF2FF",clearable:""},null,8,["modelValue"])]),_:1}),o(_,{cols:"12",md:"3"},{default:r(()=>[o(p,{modelValue:t.value,"onUpdate:modelValue":[s[1]||(s[1]=l=>t.value=l),u],items:f,"item-title":"text","item-value":"value",label:"Status",variant:"outlined",density:"comfortable",class:"filter-select","bg-color":"rgba(45, 55, 75, 0.4)",color:"#42DDF2FF",clearable:""},null,8,["modelValue"])]),_:1}),o(_,{cols:"12",md:"3"},{default:r(()=>[o(p,{modelValue:e.value,"onUpdate:modelValue":[s[2]||(s[2]=l=>e.value=l),u],items:y,"item-title":"text","item-value":"value",label:"Format",variant:"outlined",density:"comfortable","bg-color":"rgba(45, 55, 75, 0.4)",color:"#42DDF2FF",clearable:""},null,8,["modelValue"])]),_:1})]),_:1}))}}),z=F(U,[["__scopeId","data-v-439577c6"]]),T={class:"tournament-card"},O={class:"tournament-content"},R={class:"tournament-header"},j={class:"tournament-title"},k={class:"format-tag"},A={class:"tournament-info"},I={class:"info-section"},N={class:"info-section"},P={class:"info-section"},$=V({__name:"TournamentCard",props:{tournament:{}},setup(x){const c=t=>t.split("_").map(e=>e.charAt(0).toUpperCase()+e.slice(1)).join(" "),d=(t,e)=>{const m=g(new Date(t),"dd MMM yyyy"),f=g(new Date(e),"dd MMM yyyy");return`${m} / ${f}`},n=t=>t.split(" ").map(e=>e.charAt(0).toUpperCase()+e.slice(1)).join(" ");return(t,e)=>(h(),B("div",T,[a("div",O,[a("div",R,[a("h3",j,i(t.tournament.title),1),a("div",k,i(c(t.tournament.tournament_format).toUpperCase()),1)]),a("div",A,[a("div",I,[o(b,{icon:"mdi-calendar",class:"mr-2 info-icon"}),a("span",null,i(d(t.tournament.start_date,t.tournament.end_date)),1)]),a("div",N,[o(b,{icon:"mdi-flag",class:"mr-2 info-icon"}),a("span",null,"Stage: "+i(n(t.tournament.current_stage)),1)]),a("div",P,[o(b,{icon:"mdi-account-group",class:"mr-2 info-icon"}),a("span",null,i(t.tournament.number_of_teams)+" teams",1)])]),o(S,{class:"view-details-btn",variant:"outlined",to:"/events/"+t.tournament.id},{default:r(()=>e[0]||(e[0]=[M(" View Details ")])),_:1},8,["to"])])]))}}),H=F($,[["__scopeId","data-v-9d84683e"]]);export{z as F,H as T};