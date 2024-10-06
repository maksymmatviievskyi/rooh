function sdpFilterCodec(kind, codec, realSdp) {
  const codecRegex = new RegExp(`a=rtpmap:([0-9]+) ${escapeRegExp(codec)}`);
  const rtxRegex = new RegExp("a=fmtp:(\\d+) apt=(\\d+)\r$");
  const videoRegex = new RegExp(`(m=${kind} .*?)( ([0-9]+))*\\s*$`);
  const skipRegex = /a=(fmtp|rtcp-fb|rtpmap):([0-9]+)/;

  const allowed = [];

  const filterLines = (isKind, lines) => {
    let filteredSdp = "";
    for (let i = 0; i < lines.length; i++) {
      if (isKind && lines[i].startsWith(`m=${kind} `)) {
        isKind = false;
      }

      const skipMatch = lines[i].match(skipRegex);
      if (skipMatch && !allowed.includes(parseInt(skipMatch[2]))) {
        continue;
      } else if (isKind && lines[i].match(videoRegex)) {
        filteredSdp +=
          lines[i].replace(videoRegex, `$1 ${allowed.join(" ")}`) + "\n";
      } else {
        filteredSdp += lines[i] + "\n";
      }
    }
    return filteredSdp;
  };

  let isKind = false;
  const lines = realSdp.split("\n");
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].startsWith(`m=${kind} `)) {
      isKind = true;
    } else if (isKind && lines[i].startsWith("m=")) {
      isKind = false;
    }

    if (isKind) {
      const match = lines[i].match(codecRegex);
      if (match) {
        allowed.push(parseInt(match[1]));
      }

      const rtxMatch = lines[i].match(rtxRegex);
      if (rtxMatch && allowed.includes(parseInt(rtxMatch[2]))) {
        allowed.push(parseInt(rtxMatch[1]));
      }
    }
  }

  return filterLines(true, lines);
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); // $& means the whole matched string
}

export { sdpFilterCodec };
