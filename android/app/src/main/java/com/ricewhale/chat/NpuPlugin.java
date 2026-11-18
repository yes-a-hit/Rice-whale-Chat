package com.ricewhale.chat;

import android.os.Build;
import android.util.Log;

import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Hexagon NPU 桥。
 *
 * 浏览器层拿不到 NPU：Android WebView 不支持 WebNN，Chrome for Android 的 WebNN 也只有
 * cpu/gpu 两种 deviceType。骁龙的 Hexagon 只能从原生代码走 QNN（AI Engine Direct）。
 * 这个插件是唯一入口，JS 侧通过 Capacitor 调用。
 *
 * 当前能力：
 *   - available()  报告运行时状态（ORT 是否打进包、QNN HTP 库能否加载、SoC 型号、ABI）
 *   - providers()  列出 ORT 编译进来的 Execution Provider
 * 模型加载与推理在后续版本接（需要先把目标模型转成 QNN 能跑的 ONNX）。
 */
@CapacitorPlugin(name = "Npu")
public class NpuPlugin extends Plugin {

    private static final String TAG = "RiceWhaleNpu";

    /** 尝试加载 QNN 的 HTP 后端库；能加载说明包里带了 Hexagon 运行时 */
    private boolean canLoadQnn() {
        String[] libs = {"QnnHtp", "QnnHtpV73Skel", "QnnHtpV69Skel", "QnnSystem"};
        for (String lib : libs) {
            try {
                System.loadLibrary(lib);
                Log.i(TAG, "loaded " + lib);
                return true;
            } catch (Throwable error) {
                Log.i(TAG, "cannot load " + lib + ": " + error.getMessage());
            }
        }
        return false;
    }

    @PluginMethod
    public void available(PluginCall call) {
        JSObject result = new JSObject();
        boolean ort = false;
        try {
            Class.forName("ai.onnxruntime.OrtEnvironment");
            ort = true;
        } catch (Throwable ignored) {
            // 没打进包就是 false，不抛
        }

        JSArray abis = new JSArray();
        for (String abi : Build.SUPPORTED_ABIS) {
            abis.put(abi);
        }

        result.put("ort", ort);
        result.put("qnnLibrary", ort && canLoadQnn());
        result.put("abi", Build.SUPPORTED_ABIS.length > 0 ? Build.SUPPORTED_ABIS[0] : "");
        result.put("abis", abis);
        result.put("device", Build.MODEL);
        result.put("manufacturer", Build.MANUFACTURER);
        result.put("sdk", Build.VERSION.SDK_INT);
        // SoC 型号要 API 31+；老系统返回 unknown，不影响判断
        result.put("soc", Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ? Build.SOC_MODEL : "unknown");
        result.put("socManufacturer",
                Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ? Build.SOC_MANUFACTURER : "unknown");
        call.resolve(result);
    }

    @PluginMethod
    public void providers(PluginCall call) {
        JSObject result = new JSObject();
        List<String> names = new ArrayList<>();
        try {
            Class<?> environment = Class.forName("ai.onnxruntime.OrtEnvironment");
            Object instance = environment.getMethod("getEnvironment").invoke(null);
            Map<?, ?> providers =
                    (Map<?, ?>) environment.getMethod("getAvailableProviders").invoke(instance);
            if (providers != null) {
                for (Object key : providers.keySet()) {
                    names.add(String.valueOf(key));
                }
            }
        } catch (Throwable error) {
            result.put("error", String.valueOf(error.getMessage()));
        }
        JSArray list = new JSArray();
        for (String name : names) {
            list.put(name);
        }
        result.put("providers", list);
        call.resolve(result);
    }
}
