const { Client } = require('./node_modules/pg');

const SUPABASE_KEY = process.env.SUPA_KEY;
const PROJECT_REF = 'etexdfjpjvfpptselwdi';

const client = new Client({
  connectionString: `postgresql://postgres.${PROJECT_REF}:${SUPABASE_KEY}@aws-0-sa-east-1.pooler.supabase.com:6543/postgres`,
  ssl: { rejectUnauthorized: false },
  connectionTimeoutMillis: 10000,
});

async function main() {
  try {
    await client.connect();
    console.log('Conectado ao Supabase!');
    const res = await client.query('SELECT version()');
    console.log(res.rows[0].version);
    await client.end();
  } catch (err) {
    console.error('Erro:', err.message);
  }
}

main();
