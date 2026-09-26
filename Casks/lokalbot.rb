cask "lokalbot" do
  version "0.9.1"
  sha256 "9eaf90312935d52d903a31ce669edac9fe55bc7286ff14ae51697549121c679f"

  url "https://github.com/stevyhacker/lokalbot/releases/download/v#{version}/LokalBot.dmg"
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
