cask "lokalbot" do
  version "0.12.1"
  sha256 "8a14f94890b0333a3d20e78f9206198f060fce90783267e1e3e0aaeb37d450a9"

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
