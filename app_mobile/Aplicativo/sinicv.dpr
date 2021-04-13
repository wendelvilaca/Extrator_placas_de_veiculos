program sinicv;

uses
  System.StartUpCopy,
  FMX.Forms,
  GrantPermission in 'GrantPermission.pas',
  MainForm in 'MainForm.pas' {Form1},
  Service.QueryPlate in 'Service\Service.QueryPlate.pas',
  Android.JNI.Toast in 'PlatformHelper\Android\Android.JNI.Toast.pas',
  Model.QueryPlate in 'Model\Model.QueryPlate.pas',
  Frame.ConnectionSettings in 'Frame\Frame.ConnectionSettings.pas' {ConnectionSettingsFrame: TFrame},
  Frame.HistoricoConsulta in 'Frame\Frame.HistoricoConsulta.pas' {QueryHistoryFrame: TFrame},
  Frame.PhotoEffects in 'Frame\Frame.PhotoEffects.pas' {PhotoEffectsFrame: TFrame},
  Frame.PhotoOptions in 'Frame\Frame.PhotoOptions.pas' {PhotoOptionsFrame: TFrame},
  Frame.VehiclePlate in 'Frame\Frame.VehiclePlate.pas' {VehiclePlateFrame: TFrame},
  DataAccess.Connection in 'DataAccess\DataAccess.Connection.pas' {ConnectionDataAccess: TDataModule},
  DataAccess.Initialize in 'DataAccess\DataAccess.Initialize.pas',
  DataAccess.Interfaces in 'DataAccess\DataAccess.Interfaces.pas',
  DataAccess.Script in 'DataAccess\DataAccess.Script.pas',
  DataAccess.Script01 in 'DataAccess\DataAccess.Script01.pas',
  DataAccess.Settings in 'DataAccess\DataAccess.Settings.pas' {SettingsDataAccess: TDataModule},
  Proxy.QueryPlate in 'Proxy\Proxy.QueryPlate.pas' {QueryPlateProxy: TDataModule},
  Proxy.QueryDetran in 'Proxy\Proxy.QueryDetran.pas' {QueryDetranProxy: TDataModule},
  Model.QueryDetran in 'Model\Model.QueryDetran.pas',
  Service.QueryDetran in 'Service\Service.QueryDetran.pas',
  Frame.VehicleDetran in 'Frame\Frame.VehicleDetran.pas' {VehicleDetranFrame: TFrame};

{$R *.res}

begin
  Application.Initialize;
  Application.CreateForm(TConnectionDataAccess, ConnectionDataAccess);
  Application.CreateForm(TForm1, Form1);
  Application.CreateForm(TQueryPlateProxy, QueryPlateProxy);
  Application.CreateForm(TQueryDetranProxy, QueryDetranProxy);
  Application.Run;
end.
