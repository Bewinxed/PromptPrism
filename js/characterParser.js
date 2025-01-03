import { app } from "../../scripts/app.js";
import { ProviderToModels } from "./modelConfig.js";

app.registerExtension({
    name: "CharacterParser",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "CharacterPromptParser") {
            // Save original widget drawing
            const onDrawWidgets = nodeType.prototype.onDrawWidgets;
            
            nodeType.prototype.onDrawWidgets = function(...args) {
                onDrawWidgets?.apply(this, args);
                
                const provider = this.widgets.find(w => w.name === "provider");
                const model = this.widgets.find(w => w.name === "model");
                
                if (provider && model) {
                    model.options = ProviderToModels[provider.value];
                }
            };

            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function(...args) {
                const r = onNodeCreated?.apply(this, args);
                
                const provider = this.widgets.find(w => w.name === "provider");
                const model = this.widgets.find(w => w.name === "model");
                
                provider.callback = () => {
                    model.options = ProviderToModels[provider.value];
                    model.value = model.options[0];
                    app.graph.setDirtyCanvas(true);
                };
                
                return r;
            };
        }
    }
});