cask "lokalbot" do
  version "0.11.5"
  sha256 "7b226418066f41295afe339fe826295c81c89b480b1411cc9966a8921133a2d6"

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
