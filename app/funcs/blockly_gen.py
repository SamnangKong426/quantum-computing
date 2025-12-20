import streamlit.components.v1 as components


def blockly_ui():
    html_content = f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <script src="https://unpkg.com/blockly/blockly_compressed.js"></script>
    <script src="https://unpkg.com/blockly/blocks_compressed.js"></script>
    <script src="https://unpkg.com/blockly/python_compressed.js"></script>
    <script src="https://unpkg.com/blockly/msg/en.js"></script>
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
    />
    <style>
      body {{
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: #ffffff;
      }}
      #blocklyDiv {{
        height: 100vh;
        width: 100vw;
      }}
      /* Makes our label white. */
      .blocklyToolboxCategoryLabel {{
        color: #fff;
        padding-top: 10px;
      }}
      /* Adds padding around the group of categories and separators. */
      .blocklyToolboxCategoryGroup {{
        padding: 0.5em;
      }}
      /* Adds space between the categories, rounds the corners and adds space around the label. */
      .blocklyToolboxCategory {{
        padding: 5px;
        margin-bottom: 0.5em;
        border-radius: 4px;
      }}
      /* Changes color of the icon to white. */
      .customIcon {{
        color: #fff;
      }}
      /* Stacks the icon on top of the label. */
      .blocklyTreeRowContentContainer {{
        display: flex;
        flex-direction: column;
        align-items: center;
      }}
      .blocklyToolboxCategory {{
        height: initial;
      }}

      .button-container {{
        position: absolute; 
        top: 10px; 
        right: 20px; 
        z-index: 100; 
        display: flex; 
        gap: 0.5rem;
      }}

      .gui-btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.5rem;
        margin: 0px;
        line-height: 1.6;
        color: rgb(49, 51, 63); /* Streamlit text color */
        background-color: rgb(255, 255, 255);
        border: 1px solid rgba(49, 51, 63, 0.2);
        cursor: pointer;
        font-family: "Source Sans Pro", sans-serif;
        font-size: 1rem;
        transition: border-color 200ms ease 0s, background-color 200ms ease 0s, color 200ms ease 0s;
        text-decoration: none;
      }}

      .gui-btn:hover {{
        border-color: rgb(255, 75, 75); /* Streamlit red accent */
        color: rgb(255, 75, 75);
        background-color: rgb(255, 255, 255);
      }}

      .gui-btn:active {{
        background-color: rgb(255, 75, 75);
        color: white;
      }}

      .gui-btn i {{
        margin-right: 0.5rem;
      }}
      
      /* Toolbox Styles */
      .blocklyToolboxCategoryLabel {{ 
        color: #fff; 
        padding-top: 10px; }}
      .blocklyToolboxCategoryGroup {{ 
        padding: 0.5em; }}
      .blocklyToolboxCategory {{ 
        padding: 5px; 
        margin-bottom: 0.5em; 
        border-radius: 4px; 
        height: initial; }}
      .customIcon {{ 
        color: #fff; 
        }}
      .blocklyTreeRowContentContainer {{ 
        display: flex; 
        flex-direction: 
        column; 
        align-items: center; }}      
    </style>
  </head>
  <body>
    <div class="button-container">
        <button class="gui-btn" onclick="saveWorkspace()"> 
            <i class="fa fa-download"></i> Save JSON
        </button>
        <button class="gui-btn" onclick="document.getElementById('loadInput').click()"> 
            <i class="fa fa-upload"></i> Load JSON
        </button>
        <input type="file" id="loadInput" style="display:none" onchange="loadWorkspace(event)" accept=".json">
    </div>
    
    <div id="blocklyDiv"></div>

    <xml
      xmlns="https://developers.google.com/blockly/xml"
      id="toolbox-categories"
      style="display: none"
    >
      <!-- <toolboxlabel name="Custom Toolbox" colour="darkslategrey"></toolboxlabel> -->
      <category
        css-icon="customIcon fa fa-filter"
        name="Logic"
        categorystyle="logic_category"
      >
        <block type="controls_if"></block>
        <block type="logic_compare"></block>
        <block type="logic_operation"></block>
        <block type="logic_negate"></block>
        <block type="logic_boolean"></block>
        <block type="logic_null" disabled="true"></block>
        <block type="logic_ternary"></block>
      </category>
      <category name="Loops" css-icon="customIcon fa fa-refresh" categorystyle="loop_category">
        <block type="controls_repeat_ext">
          <value name="TIMES">
            <shadow type="math_number">
              <field name="NUM">10</field>
            </shadow>
          </value>
        </block>
        <block type="controls_repeat" disabled="true"></block>
        <block type="controls_whileUntil"></block>
        <block type="controls_for">
          <value name="FROM">
            <shadow type="math_number">
              <field name="NUM">1</field>
            </shadow>
          </value>
          <value name="TO">
            <shadow type="math_number">
              <field name="NUM">10</field>
            </shadow>
          </value>
          <value name="BY">
            <shadow type="math_number">
              <field name="NUM">1</field>
            </shadow>
          </value>
        </block>
        <block type="controls_forEach"></block>
        <block type="controls_flow_statements"></block>
      </category>
      <category name="Math" css-icon="customIcon fa fa-calculator" categorystyle="math_category">
        <block type="math_number" gap="32">
          <field name="NUM">123</field>
        </block>
        <block type="math_arithmetic">
          <value name="A">
            <shadow type="math_number">
              <field name="NUM">1</field>
            </shadow>
          </value>
          <value name="B">
            <shadow type="math_number">
              <field name="NUM">1</field>
            </shadow>
          </value>
        </block>
        <block type="math_single">
          <value name="NUM">
            <shadow type="math_number">
              <field name="NUM">9</field>
            </shadow>
          </value>
        </block>
        <block type="math_trig">
          <value name="NUM">
            <shadow type="math_number">
              <field name="NUM">45</field>
            </shadow>
          </value>
        </block>
        <block type="math_constant"></block>
        <block type="math_number_property">
          <value name="NUMBER_TO_CHECK">
            <shadow type="math_number">
              <field name="NUM">0</field>
            </shadow>
          </value>
        </block>
        <block type="math_round">
          <value name="NUM">
            <shadow type="math_number">
              <field name="NUM">3.1</field>
            </shadow>
          </value>
        </block>
        <block type="math_on_list"></block>
        <block type="math_modulo">
          <value name="DIVIDEND">
            <shadow type="math_number">
              <field name="NUM">64</field>
            </shadow>
          </value>
          <value name="DIVISOR">
            <shadow type="math_number">
              <field name="NUM">10</field>
            </shadow>
          </value>
        </block>
        <block type="math_constrain">
          <value name="VALUE">
            <shadow type="math_number">
              <field name="NUM">50</field>
            </shadow>
          </value>
          <value name="LOW">
            <shadow type="math_number">
              <field name="NUM">1</field>
            </shadow>
          </value>
          <value name="HIGH">
            <shadow type="math_number">
              <field name="NUM">100</field>
            </shadow>
          </value>
        </block>
        <block type="math_random_int">
          <value name="FROM">
            <shadow type="math_number">
              <field name="NUM">1</field>
            </shadow>
          </value>
          <value name="TO">
            <shadow type="math_number">
              <field name="NUM">100</field>
            </shadow>
          </value>
        </block>
        <block type="math_random_float"></block>
        <block type="math_atan2">
          <value name="X">
            <shadow type="math_number">
              <field name="NUM">1</field>
            </shadow>
          </value>
          <value name="Y">
            <shadow type="math_number">
              <field name="NUM">1</field>
            </shadow>
          </value>
        </block>
      </category>
      <category name="Text" css-icon="customIcon fa fa-font" categorystyle="text_category">
        <block type="text"></block>
        <block type="text_join"></block>
        <block type="text_append">
          <value name="TEXT">
            <shadow type="text"></shadow>
          </value>
        </block>
        <block type="text_length">
          <value name="VALUE">
            <shadow type="text">
              <field name="TEXT">abc</field>
            </shadow>
          </value>
        </block>
        <block type="text_isEmpty">
          <value name="VALUE">
            <shadow type="text">
              <field name="TEXT"></field>
            </shadow>
          </value>
        </block>
        <block type="text_indexOf">
          <value name="VALUE">
            <block type="variables_get">
              <field name="VAR">text</field>
            </block>
          </value>
          <value name="FIND">
            <shadow type="text">
              <field name="TEXT">abc</field>
            </shadow>
          </value>
        </block>
        <block type="text_charAt">
          <value name="VALUE">
            <block type="variables_get">
              <field name="VAR">text</field>
            </block>
          </value>
        </block>
        <block type="text_getSubstring">
          <value name="STRING">
            <block type="variables_get">
              <field name="VAR">text</field>
            </block>
          </value>
        </block>
        <block type="text_changeCase">
          <value name="TEXT">
            <shadow type="text">
              <field name="TEXT">abc</field>
            </shadow>
          </value>
        </block>
        <block type="text_trim">
          <value name="TEXT">
            <shadow type="text">
              <field name="TEXT">abc</field>
            </shadow>
          </value>
        </block>
        <block type="text_count">
          <value name="SUB">
            <shadow type="text"></shadow>
          </value>
          <value name="TEXT">
            <shadow type="text"></shadow>
          </value>
        </block>
        <block type="text_replace">
          <value name="FROM">
            <shadow type="text"></shadow>
          </value>
          <value name="TO">
            <shadow type="text"></shadow>
          </value>
          <value name="TEXT">
            <shadow type="text"></shadow>
          </value>
        </block>
        <block type="text_reverse">
          <value name="TEXT">
            <shadow type="text"></shadow>
          </value>
        </block>
        <label text="Input/Output:" web-class="ioLabel"></label>
        <block type="text_print">
          <value name="TEXT">
            <shadow type="text">
              <field name="TEXT">abc</field>
            </shadow>
          </value>
        </block>
        <block type="text_prompt_ext">
          <value name="TEXT">
            <shadow type="text">
              <field name="TEXT">abc</field>
            </shadow>
          </value>
        </block>
      </category>
      <category name="Lists" css-icon="customIcon fa fa-list-ul" categorystyle="list_category">
        <block type="lists_create_with">
          <mutation items="0"></mutation>
        </block>
        <block type="lists_create_with"></block>
        <block type="lists_repeat">
          <value name="NUM">
            <shadow type="math_number">
              <field name="NUM">5</field>
            </shadow>
          </value>
        </block>
        <block type="lists_length"></block>
        <block type="lists_isEmpty"></block>
        <block type="lists_indexOf">
          <value name="VALUE">
            <block type="variables_get">
              <field name="VAR">list</field>
            </block>
          </value>
        </block>
        <block type="lists_getIndex">
          <value name="VALUE">
            <block type="variables_get">
              <field name="VAR">list</field>
            </block>
          </value>
        </block>
        <block type="lists_setIndex">
          <value name="LIST">
            <block type="variables_get">
              <field name="VAR">list</field>
            </block>
          </value>
        </block>
        <block type="lists_getSublist">
          <value name="LIST">
            <block type="variables_get">
              <field name="VAR">list</field>
            </block>
          </value>
        </block>
        <block type="lists_split">
          <value name="DELIM">
            <shadow type="text">
              <field name="TEXT">,</field>
            </shadow>
          </value>
        </block>
        <block type="lists_sort"></block>
        <block type="lists_reverse"></block>
      </category>
      <sep></sep>
      <category
        name="Variables"
        css-icon="customIcon fa fa-tag"
        categorystyle="variable_category"
        custom="VARIABLE"
      ></category>
      <category
        name="Functions"
        css-icon="customIcon fa fa-gears"
        categorystyle="procedure_category"
        custom="PROCEDURE"
      ></category>
      <br />
      <sep></sep>
      <category
        name="Qubits"
        css-icon="customIcon fa fa-flask"
        css-icon="customIcon fa fa-cog"
        categorystyle="logic_category"
        ><block type="quantum_circuit"></block
      ></category>
      <category
        name="Gates"
        css-icon="customIcon fa fa-microchip"
        categorystyle="logic_category"
      >
        <block type="single_qubit_gate"><field name="GATE">X</field></block>
        <block type="single_qubit_gate"><field name="GATE">Y</field></block>
        <block type="single_qubit_gate"><field name="GATE">Z</field></block>
        <block type="single_qubit_gate"><field name="GATE">H</field></block>
        <block type="two_qubit_gate"><field name="GATE">CX</field></block>
        <block type="two_qubit_gate"><field name="GATE">CZ</field></block>
        <block type="two_qubit_gate"><field name="GATE">SWAP</field></block>
        <block type="two_qubit_gate"><field name="GATE">ISSWAP</field></block>
      </category>
      <category
        name="Measure"
        css-icon="customIcon fa fa-dashboard"
        categorystyle="logic_category">
        <block type="measure_qubit"></block>
        <block type="aer_simulator"></block>
      </category>
      <category
        name="Circuit"
        css-icon="customIcon fa fa-bolt"
        categorystyle="logic_category">
        <block type="barrier"></block>
        <block type="display_circuit"></block>
        <block type="display_bloch"></block>
      </category>
    </xml>

    <script>
      /**
       * @license
       * Copyright 2020 Google LLC
       * SPDX-License-Identifier: Apache-2.0
       */

      /**
       * @fileoverview The toolbox category built during the custom toolbox codelab, in es6.
       * @author aschmiedt@google.com (Abby Schmiedt)
       */

      class CustomCategory extends Blockly.ToolboxCategory {{
        /**
         * Constructor for a custom category.
         * @override
         */
        constructor(categoryDef, toolbox, opt_parent) {{
          super(categoryDef, toolbox, opt_parent);
        }}

        /**
         * Adds the colour to the toolbox.
         * This is called on category creation and whenever the theme changes.
         * @override
         */
        addColourBorder_(colour) {{
          this.rowDiv_.style.backgroundColor = colour;
        }}

        /**
         * Sets the style for the category when it is selected or deselected.
         * @param {{boolean}} isSelected True if the category has been selected,
         *     false otherwise.
         * @override
         */
        setSelected(isSelected) {{
          // We do not store the label span on the category, so use getElementsByClassName.
          const labelDom = this.rowDiv_.getElementsByClassName(
            "blocklyToolboxCategoryLabel"
          )[0];
          if (isSelected) {{
            // Change the background color of the div to white.
            this.rowDiv_.style.backgroundColor = "white";
            // Set the colour of the text to the colour of the category.
            labelDom.style.color = this.colour_;
            this.iconDom_.style.color = this.colour_;
          }} else {{
            // Set the background back to the original colour.
            this.rowDiv_.style.backgroundColor = this.colour_;
            // Set the text back to white.
            labelDom.style.color = "white";
            this.iconDom_.style.color = "white";
          }}
          // This is used for accessibility purposes.
          Blockly.utils.aria.setState(
            /** @type {{!Element}} */ (this.htmlDiv_),
            Blockly.utils.aria.State.SELECTED,
            isSelected
          );
        }}

        /**
         * Creates the dom used for the icon.
         * @returns {{HTMLElement}} The element for the icon.
         * @override
         */
        /*createIconDom_() {{
          const iconImg = document.createElement("img");
          iconImg.src = "./logo_only.svg";
          iconImg.alt = "Blockly Logo";
          iconImg.width = "25";
          iconImg.height = "25";
          return iconImg;
        }}*/
      }}

      /**
       * @license
       * Copyright 2020 Google LLC
       * SPDX-License-Identifier: Apache-2.0
       */

      /**
       * @fileoverview The toolbox label built during the custom toolbox codelab, in es6.
       * @author aschmiedt@google.com (Abby Schmiedt)
       */

      class ToolboxLabel extends Blockly.ToolboxItem {{
        /**
         * Constructor for a label in the toolbox.
         * @param {{!Blockly.utils.toolbox.ToolboxItemInfo}} toolboxItemDef The toolbox
         *    item definition. This comes directly from the toolbox definition.
         * @param {{!Blockly.IToolbox}} parentToolbox The toolbox that holds this
         *    toolbox item.
         * @override
         */
        constructor(toolboxItemDef, parentToolbox) {{
          super(toolboxItemDef, parentToolbox);
          /**
           * The button element.
           * @type {{?HTMLLabelElement}}
           */
          this.label = null;
        }}

        /**
         * Init method for the label.
         * @override
         */
        init() {{
          // Create the label.
          this.label = document.createElement("label");
          // Set the name.
          this.label.textContent = this.toolboxItemDef_["name"];
          // Set the color.
          this.label.style.color = this.toolboxItemDef_["colour"];
          // Any attributes that begin with css- will get added to a cssconfig.
          const cssConfig = this.toolboxItemDef_["cssconfig"];
          // Add the class.
          if (cssConfig) {{
            this.label.classList.add(cssConfig["label"]);
          }}
        }}

        /**
         * Gets the div for the toolbox item.
         * @returns {{HTMLLabelElement}} The label element.
         * @override
         */
        getDiv() {{
          return this.label;
        }}
      }}

      Blockly.registry.register(
        Blockly.registry.Type.TOOLBOX_ITEM,
        "toolboxlabel",
        ToolboxLabel
      );

      Blockly.registry.register(
        Blockly.registry.Type.TOOLBOX_ITEM,
        Blockly.ToolboxCategory.registrationName,
        CustomCategory,
        true
      );

      // --- Block Definitions ---
      Blockly.Blocks["quantum_circuit"] = {{
        init: function () {{
          this.appendDummyInput()
            .appendField("Qubit")
            .appendField(new Blockly.FieldNumber(1, 0), "QUBITS")
            .appendField("Classic")
            .appendField(new Blockly.FieldNumber(1, 0), "CLASSICAL_BITS");
          this.setNextStatement(true);
          this.setColour(160);
        }},
      }};

      Blockly.Blocks["single_qubit_gate"] = {{
        init: function () {{
          this.appendDummyInput()
            .appendField("apply")
            .appendField(
              new Blockly.FieldDropdown([
                ["X", "X"],
                ["Y", "Y"],
                ["Z", "Z"],
                ["H", "H"],
              ]),
              "GATE"
            )
            .appendField("on q[")
            .appendField(new Blockly.FieldTextInput("0"), "QUBIT")
            .appendField("]");
          this.setPreviousStatement(true);
          this.setNextStatement(true);
          this.setColour(230);
        }},
      }};

      Blockly.Blocks["two_qubit_gate"] = {{
        init: function () {{
          this.appendDummyInput()
            .appendField("apply")
            .appendField(
              new Blockly.FieldDropdown([
                ["CX", "CX"],
                ["CZ", "CZ"],
                ["SWAP", "SWAP"],
                ["ISWAP", "ISWAP"],
              ]),
              "GATE"
            )
            .appendField("control q[")
            .appendField(new Blockly.FieldTextInput("0"), "CONTROL")
            .appendField("]")
            .appendField("target q[")
            .appendField(new Blockly.FieldTextInput("1"), "TARGET")
            .appendField("]");

          this.setPreviousStatement(true);
          this.setNextStatement(true);
          this.setColour(230);
        }},
      }};

      Blockly.Blocks["aer_simulator"] = {{
        init: function () {{
          this.appendDummyInput()
            .appendField("Aer Simulator")
            .appendField(new Blockly.FieldTextInput("1024"), "SHORTS");
          this.setPreviousStatement(true);
          this.setNextStatement(true);
          this.setColour(120);
        }},
      }};

      Blockly.Blocks["measure_qubit"] = {{
        init: function () {{
          this.appendDummyInput()
            .appendField("measure q[")
            .appendField(new Blockly.FieldTextInput("0"), "QUBIT")
            .appendField("] ")
            .appendField("to q[")
            .appendField(new Blockly.FieldTextInput("0"), "CBIT")
            .appendField("]");
          this.setPreviousStatement(true);
          this.setNextStatement(true);
          this.setColour(120);
        }},
      }};

      Blockly.Blocks["barrier"] = {{
        init: function () {{
          this.appendDummyInput()
            .appendField("barrier")
          this.setPreviousStatement(true);
          this.setNextStatement(true);
          this.setColour(120);
        }},
      }};

      Blockly.Blocks["display_circuit"] = {{
        init: function () {{
          this.appendDummyInput()
            .appendField("display circuit")
          this.setPreviousStatement(true);
          this.setNextStatement(true);
          this.setColour(120);
        }},
      }};

      Blockly.Blocks["display_bloch"] = {{
        init: function () {{
          this.appendDummyInput()
            .appendField("display bloch")
          this.setPreviousStatement(true);
          this.setNextStatement(true);
          this.setColour(120);
        }},
      }};


      const pythonGenerator = python.pythonGenerator;

      pythonGenerator.forBlock["quantum_circuit"] = function (block) {{
        return (
          "from qiskit import QuantumCircuit\\n" + 
          "qc = QuantumCircuit(" +
          block.getFieldValue("QUBITS") +
          ", " +
          block.getFieldValue("CLASSICAL_BITS") +
          ")\\n"
        );
      }};

      pythonGenerator.forBlock["single_qubit_gate"] = function (block) {{
        return (
          "qc." +
          block.getFieldValue("GATE").toLowerCase() +
          "(" +
          block.getFieldValue("QUBIT") +
          ")\\n"
        );
      }};

      pythonGenerator.forBlock["two_qubit_gate"] = function (block) {{
        return (
          "qc." +
          block.getFieldValue("GATE").toLowerCase() +
          "(" +
          block.getFieldValue("CONTROL") + ", " +
          block.getFieldValue("TARGET") + 
          ")\\n"
        );
      }};

      pythonGenerator.forBlock["aer_simulator"] = function (block) {{
        const shots = block.getFieldValue("SHOTS") || 1024; 
        return (
          "from qiskit_aer import AerSimulator\\n" +
          "from qiskit.visualization import plot_histogram\\n" +
          "from qiskit import transpile\\n" +
          "backend = AerSimulator()\\n" +
          "tqc = transpile(qc, backend)\\n" +
          "job = backend.run(tqc, shots=" + shots + ")\\n" +
          "result = job.result()\\n" +
          "counts = result.get_counts()\\n\\n" +
          "plot_histogram(counts)\\n"
        );
      }};

      pythonGenerator.forBlock["measure_qubit"] = function (block) {{
        return (
          "qc.measure(" +
          block.getFieldValue("QUBIT") +
          ", " +
          block.getFieldValue("CBIT") +
          ")\\n"
        );
      }};

      pythonGenerator.forBlock["barrier"] = function (block) {{
        return (
          "qc.barrier()\\n"
        );
      }};

      pythonGenerator.forBlock["display_circuit"] = function (block) {{
        return (
          "from qiskit.visualization import circuit_drawer\\n" +
          "import matplotlib.pyplot as plt\\n" +
          "circuit = circuit_drawer(qc, output='mpl')\\n" +
          "plt.show()\\n"
        );
      }};

      pythonGenerator.forBlock["display_bloch"] = function (block) {{
        return (
          "from qiskit.quantum_info import Statevector\\n" +
          "from qiskit.visualization import plot_bloch_multivector\\n" +
          "state = Statevector(qc)\\n" +
          "bloch = plot_bloch_multivector(state)\\n" +
          "plt.show()\\n"
        );
      }};
      

      const workspace = Blockly.inject("blocklyDiv", {{
        theme: Blockly.Themes.Modern,
        toolbox: document.getElementById("toolbox-categories"),
        zoom:
         {{controls: true,
          wheel: true,
          startScale: 1.0,
          maxScale: 3,
          minScale: 1,
          scaleSpeed: 1.2,
          pinch: true}},
        trashcan: true,
      }});

      window.saveWorkspace = function() {{
        const state = Blockly.serialization.workspaces.save(workspace);
        const data = JSON.stringify(state);
        const blob = new Blob([data], {{type: "application/json"}});
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = "quantum_edu.json";
        link.click();
      }};

      window.loadWorkspace = function(event) {{
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function(e) {{
          const state = JSON.parse(e.target.result);
          Blockly.serialization.workspaces.load(state, workspace);
          syncToStreamlit();
        }};
        reader.readAsText(file);
      }};


      // --- Update Logic ---
      function syncToStreamlit() {{
        const code = pythonGenerator.workspaceToCode(workspace);
        console.log(code)
        // We use URL search params to send the code back to the parent Streamlit app
        const parentUrl = new URL(window.parent.location.href);
        parentUrl.searchParams.set("code", code);
        window.parent.history.replaceState({{}}, "", parentUrl);

        // Trigger a light refresh if needed, or use postMessage for more advanced setups
        window.parent.postMessage(
          {{ type: "streamlit:setComponentValue", value: code }},
          "*"
        );
      }}

      workspace.addChangeListener((e) => {{
        if (!e.isUiEvent) syncToStreamlit();
      }});
    </script>
  </body>
</html>
"""
    components.html(html_content, height=730)
