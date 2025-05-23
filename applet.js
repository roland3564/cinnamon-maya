const Applet = imports.ui.applet;
const GLib = imports.gi.GLib;
const Settings = imports.ui.settings;
const Lang = imports.lang;

class MyApplet extends Applet.TextApplet {
    constructor(metadata, orientation, panelHeight, instanceId) {
        super(orientation, panelHeight, instanceId);

        this.settings = new Settings.AppletSettings(this, metadata.uuid, instanceId);
        this.settings.bind("show_long_count", "show_long_count");
        this.settings.bind("show_tzolkin", "show_tzolkin");
        this.settings.bind("show_haab", "show_haab");
        this.settings.bind("day_offset", "day_offset");
        this.settings.bind("sunrise_hour", "sunrise_hour");

        this.refresh();
    }

    refresh() {
        let output = this.runPythonScript();
        this.set_applet_label(output);

        GLib.timeout_add_seconds(0, 300, () => {
            this.refresh();
            return true;
        });
    }

    runPythonScript() {
        try {
            // Write current settings to config file
            const config = {
                show_long_count: this["show_long_count"],
                show_tzolkin: this["show_tzolkin"],
                show_haab: this["show_haab"],
                day_offset: this["day_offset"],
                sunrise_hour: this["sunrise_hour"]
            };
            const configPath = GLib.get_home_dir() + "/.local/share/cinnamon/applets/mayan-calendar@n1/config.json";
            GLib.file_set_contents(configPath, JSON.stringify(config));

            let [success, stdout, stderr] = GLib.spawn_sync(
                null,
                ["python3", "/home/n1/.local/share/cinnamon/applets/mayan-calendar@n1/mayan_date.py"],
                null,
                GLib.SpawnFlags.SEARCH_PATH,
                null
            );

            return stdout.toString().trim();
        } catch (e) {
            global.log("Mayan Calendar Applet Error: " + e.message);
            return "Error";
        }
    }
}

function main(metadata, orientation, panelHeight, instanceId) {
    return new MyApplet(metadata, orientation, panelHeight, instanceId);
}
