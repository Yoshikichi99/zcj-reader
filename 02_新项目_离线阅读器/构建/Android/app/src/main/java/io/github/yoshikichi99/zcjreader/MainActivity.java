package io.github.yoshikichi99.zcjreader;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.Insets;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.ViewGroup;
import android.view.WindowInsets;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;

/**
 * 壳只做四件事：
 * 1. 起一个 WebView，把 https://appassets.androidplatform.net/ 映射到 APK 的 assets/；
 * 2. 不改前端代码——与 Windows 版共用同一份 前端/proto；
 * 3. 返回键 → history.back()，到首页再按才退出；
 * 4. Android 15+ 强制 edge-to-edge，这里给 WebView 补状态栏/导航栏安全区。
 *
 * 故意不引 AndroidX：资源映射自己实现（shouldInterceptRequest），
 * 比 WebViewAssetLoader 少一个依赖，APK 也小一点。
 */
public class MainActivity extends Activity {

    private static final String HOST = "appassets.androidplatform.net";
    private static final String ENTRY = "https://" + HOST + "/index.html";

    private WebView web;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        web = new WebView(this);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);       // 繁简选择、阅读记录用 localStorage
        // 必须开：否则 index.html 的 viewport 不生效，页面按桌面宽度布局、横向溢出
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setTextZoom(100);                 // 不受系统字体缩放影响，字号由页面自己控
        s.setAllowFileAccess(false);
        // 资源都在 APK 里，没有联网收益；不关缓存的话升级后仍会读到旧的 style.css/app.js
        s.setCacheMode(WebSettings.LOAD_NO_CACHE);
        s.setAllowContentAccess(false);
        s.setSupportZoom(false);            // 缩放由字号档位控制，不用双指
        s.setBuiltInZoomControls(false);
        s.setMediaPlaybackRequiresUserGesture(true);
        web.setBackgroundColor(0xFFEFFFDE); // 与页面底色一致，避免白闪
        web.setWebViewClient(new LocalClient());

        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(0xFFEFFFDE);
        root.addView(web, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        setContentView(root);
        applyInsets(root);

        web.loadUrl(ENTRY);
    }

    /**
     * Android 15（API 35）起，targetSdk>=35 的窗口强制 edge-to-edge。
     * 注意：WebView 的 padding 不会缩进网页视口（页面仍按整块 View 布局），
     * 所以这里给 WebView 设真实的外边距，让网页视口本身落在安全区内，
     * 顶栏 position:sticky 才会自然地停在状态栏下方。
     */
    private void applyInsets(FrameLayout root) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            getWindow().setDecorFitsSystemWindows(false);
            root.setOnApplyWindowInsetsListener((v, wi) -> {
                Insets bars = wi.getInsets(
                        WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                Insets gestures = wi.getInsets(WindowInsets.Type.mandatorySystemGestures());
                ViewGroup.LayoutParams lp = web.getLayoutParams();
                if (lp instanceof ViewGroup.MarginLayoutParams) {
                    ViewGroup.MarginLayoutParams m = (ViewGroup.MarginLayoutParams) lp;
                    m.topMargin = bars.top;
                    m.leftMargin = bars.left;
                    m.rightMargin = bars.right;
                    m.bottomMargin = Math.max(bars.bottom, gestures.bottom);
                    web.setLayoutParams(m);
                }
                return wi;
            });
            root.requestApplyInsets();
        }
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) {
            web.goBack();
        } else {
            super.onBackPressed();
        }
    }

    private class LocalClient extends WebViewClient {

        @Override
        public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest req) {
            Uri u = req.getUrl();
            if (!HOST.equals(u.getHost())) return null;
            String path = u.getPath();
            if (path == null || path.length() < 2) return null;
            String asset = path.substring(1);       // "/data/toc.json.gz" -> "data/toc.json.gz"
            // 打包时 .gz 被改名成 .gz.bin（躲开 AGP 的自动解压），这里映射回去
            if (asset.endsWith(".gz")) asset = asset + ".bin";
            try {
                InputStream in = getAssets().open(asset);
                String mime = guessMime(asset);
                // 文本给编码，二进制给 null（否则 WebView 会按文本转码）
                String encoding = isText(mime) ? "utf-8" : null;
                return new WebResourceResponse(mime, encoding, in);
            } catch (IOException e) {
                return null;                        // 交给默认处理（表现为 404）
            }
        }

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest req) {
            Uri u = req.getUrl();
            if (HOST.equals(u.getHost())) return false;   // 站内 hash 路由，交给页面
            // 离线版不申请 INTERNET 权限，外部链接也不放行
            Toast.makeText(MainActivity.this,
                    "離線版不連網，外部連結已停用", Toast.LENGTH_SHORT).show();
            return true;
        }
    }

    private static boolean isText(String mime) {
        return mime.startsWith("text/") || mime.equals("application/javascript")
                || mime.equals("application/json");
    }

    private static String guessMime(String name) {
        String n = name.toLowerCase();
        if (n.endsWith(".html") || n.endsWith(".htm")) return "text/html";
        if (n.endsWith(".js")) return "application/javascript";
        if (n.endsWith(".css")) return "text/css";
        if (n.endsWith(".json")) return "application/json";
        if (n.endsWith(".json.gz") || n.endsWith(".gz")) return "application/gzip";
        if (n.endsWith(".jpg") || n.endsWith(".jpeg")) return "image/jpeg";
        if (n.endsWith(".png")) return "image/png";
        if (n.endsWith(".gif")) return "image/gif";
        if (n.endsWith(".svg")) return "image/svg+xml";
        if (n.endsWith(".woff2")) return "font/woff2";
        return "application/octet-stream";
    }
}
