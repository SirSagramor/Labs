'use strict';

const en = [];
for (let i = 0; i < 26; i++) {
  en.push(new Array());
}
for (let k = 0; k < 26; k++) {
  for (let i = 0; i < 26; i++) {
    en[k].push(String.fromCharCode((i + k) % 26 + 97));
  }
}

const cipher = function(key, word) {

  const arrkey = key.toLowerCase().split('');
  const arrword = word.toLowerCase().split('');
  if (~arrkey.indexOf(' ') || ~arrword.indexOf(' ')) {
    throw new Error('WITHOUT TABS!');
  }
  const out = [];

  for (let i = 0; arrkey.length < arrword.length; i++) {
    arrkey.push(arrkey[i]);
  }
  for (let i = 0; i < arrkey.length; i++) {
    const j = arrword[i].charCodeAt(0) - 97;
    const k = arrkey[i].charCodeAt(0) - 97;
    out.push(en[k][j]);
  }
  const output = out.join('');
  return output;
};


console.log(cipher('kawabanga', 'IHateEverythingAboutYou'));
