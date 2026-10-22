cask "lokalbot" do
  version "0.11.2"
  sha256 "f1f5c3654fa7b344572794a793e8505f4359b6bb7ca0c67f0d6c55d8b560c4a8"

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
