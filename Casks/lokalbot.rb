cask "lokalbot" do
  version "0.11.4"
  sha256 "713041a3343eb4ba085973a391240a03cef836f286b47c1be0df7497eb8d6783"

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
