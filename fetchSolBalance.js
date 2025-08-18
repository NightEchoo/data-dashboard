const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

// Solscan URL
const solscanUrl = 'https://solscan.io/account/A9NBEQeCYzvqidFnh7UVZsBrW2T5df4cqnBjxCBQRJ88';

// 抓取 Solscan 页面
axios.get(solscanUrl).then((response) => {
  const $ = cheerio.load(response.data);

  // 提取 SOL 余额
  const solBalanceText = $('span[data-qa="sol_balance"]').text().trim();
  const solBalance = parseFloat(solBalanceText.replace('SOL', '').trim());

  // 转换为美元（示例固定汇率）
  const solToUsd = 182.93;
  const solInUsd = (solBalance * solToUsd).toFixed(2);

  // 将数据保存为 JSON 文件
  const solData = {
    solBalance: solBalance,
    solInUsd: solInUsd
  };

  fs.writeFileSync('solBalance.json', JSON.stringify(solData, null, 2));

  console.log('Data fetched and saved:', solData);
}).catch((error) => {
  console.error('Error fetching data:', error);
});
