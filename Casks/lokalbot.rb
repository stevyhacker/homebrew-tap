cask "lokalbot" do
  version "0.12.0"
  sha256 "95d8111c1fb4989f868f6aa4c0b5837548e1226890b8cb2f78fdd337f9894ca6"

  url "https://github.com/stevyhacker/lokalbot/releases/download/v#{version}/LokalBot-#{version}-macos-arm64.dmg"
  name "LokalBot"
  desc "Find what you said or saw on your Mac"
  homepage "https://www.lokalbot.com/"

  livecheck do
    url :url
    strategy :github_releases
  end

  auto_updates true
  depends_on arch: :arm64
  depends_on macos: :sequoia

  app "LokalBot.app"

  zap trash: [
    "~/Library/Application Support/me.dotenv.LokalBot",
    "~/Library/Preferences/me.dotenv.LokalBot.plist",
  ]
end
