// https://vitejs.dev/config/
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000, // 开发服务器端口
    proxy:{
      '/api':
      {
        target: 'http://localhost:5000',
        changeOrigin: true // 改变请求头中的Host字段
      }
    }
  },
  
});
